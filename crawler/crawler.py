import requests
import json
import os
import time
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html"
OUTPUT_DIR = "/app/data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fahasa_data.json")
MAX_PAGES = 5  # Limit to 5 pages for faster testing

def get_page(url):
    """Fetch a page from Fahasa with retry logic."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
    
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            retry_count += 1
            logger.warning(f"Request failed ({retry_count}/{max_retries}): {e}")
            time.sleep(2)  # Wait before retrying
    
    logger.error(f"Failed to fetch {url} after {max_retries} attempts")
    return None

def parse_books(html):
    """Parse HTML to extract book details from Fahasa website."""
    soup = BeautifulSoup(html, 'lxml')
    books = []
    
    # Log the HTML structure to debug
    logger.info("Analyzing page structure...")
    
    # Find the products container
    products_container = soup.select_one("ul#products_grid.products-grid")
    if not products_container:
        logger.warning("Could not find products grid container")
        return books
    
    # Find all book items (li elements that are direct children of the products grid)
    book_elements = products_container.find_all("li", recursive=False)
    
    logger.info(f"Found {len(book_elements)} book elements on page")
    
    for book in book_elements:
        try:
            # Extract title
            title_element = book.select_one("h2.product-name-no-ellipsis a")
            if not title_element:
                # Try alternative selector
                title_element = book.select_one("a.product-image")
                
            if title_element:
                # Get the title text, cleaning up any extra elements
                title = title_element.get_text(strip=True)
                # Remove trending icon text if present
                if title_element.select_one("img.label-tagname"):
                    title = ' '.join(title.split()[1:])
                
                # Get book URL
                book_url = title_element.get('href', '')
                if not book_url.startswith('http'):
                    book_url = f"https://www.fahasa.com{book_url}" if book_url.startswith('/') else f"https://www.fahasa.com/{book_url}"
            else:
                logger.warning("Could not find title element, skipping book")
                continue  # Skip if no title
            
            # Extract price
            special_price_element = book.select_one("p.special-price span.price")
            if special_price_element:
                price = special_price_element.get_text(strip=True)
            else:
                price_element = book.select_one("span.price")
                price = price_element.get_text(strip=True) if price_element else "N/A"
            
            # Extract original price
            old_price_element = book.select_one("p.old-price span.price")
            old_price = old_price_element.get_text(strip=True) if old_price_element else None
            
            # Extract discount percentage
            discount_element = book.select_one("span.discount-percent")
            discount = discount_element.get_text(strip=True) if discount_element else None
            
            # Extract rating
            rating_element = book.select_one("div.rating")
            if rating_element and rating_element.has_attr('style'):
                # Extract percentage from style="width:XX%"
                rating_style = rating_element['style']
                rating_percentage = rating_style.split(':')[1].strip().rstrip('%')
                rating = float(rating_percentage) / 20  # Convert percentage to 5-star scale
            else:
                rating_text_element = book.select_one("div.rating-links")
                rating = float(rating_text_element.get_text(strip=True)) if rating_text_element and rating_text_element.get_text(strip=True) != '0' else 0
            
            # Extract image URL
            img_element = book.select_one("span.product-image img.lazyload")
            img_url = None
            if img_element:
                # Try different attributes for image
                if img_element.has_attr('data-src'):
                    img_url = img_element['data-src']
                elif img_element.has_attr('src'):
                    img_url = img_element['src']
            
            # Build book data
            book_data = {
                "title": title,
                "price": price,
                "original_price": old_price,
                "discount": discount,
                "rating": rating,
                "url": book_url,
                "image_url": img_url
            }
            
            books.append(book_data)
            logger.debug(f"Extracted book: {title}")
            
        except Exception as e:
            logger.warning(f"Error parsing book: {e}")
    
    return books

def get_next_page_url(html, current_url):
    """Extract the URL for the next page."""
    soup = BeautifulSoup(html, 'lxml')
    
    # Look for the pagination section
    pagination = soup.select_one("div.pages")
    if not pagination:
        return None
    
    # Find the next button
    next_page_link = soup.find("a", onclick=lambda x: x and "catalog_ajax.Page_change('next')" in x)
    if next_page_link:
        # Get current page number from various possible sources
        current_page_element = soup.select_one("li.current a")
        if current_page_element:
            try:
                current_page = int(current_page_element.get_text(strip=True))
                next_page = current_page + 1
                
                # Construct next page URL
                base_url = current_url.split('?')[0] if '?' in current_url else current_url
                # Check if URL ends with .html
                if not base_url.endswith('.html'):
                    base_url = f"{base_url}.html"
                return f"{base_url}?p={next_page}"
            except (ValueError, TypeError) as e:
                logger.warning(f"Error parsing pagination: {e}")
                return None
    
    return None

def crawl_fahasa():
    """Main crawler function to fetch books from Fahasa."""
    all_books = []
    url = BASE_URL
    page_count = 0
    
    logger.info("Starting Fahasa crawler")
    
    while url and page_count < MAX_PAGES:
        logger.info(f"Crawling page {page_count + 1}: {url}")
        html = get_page(url)
        
        if not html:
            logger.error(f"Failed to get page {page_count + 1}")
            break
        
        # Save the HTML for debugging if needed
        if page_count == 0:
            debug_file = os.path.join(OUTPUT_DIR, "debug_page.html")
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info(f"Saved first page HTML to {debug_file} for debugging")
        
        books = parse_books(html)
        logger.info(f"Found {len(books)} books on page {page_count + 1}")
        all_books.extend(books)
        
        # Get next page URL
        next_url = get_next_page_url(html, url)
        if next_url:
            url = next_url
            page_count += 1
            # Politeness delay
            time.sleep(2)
        else:
            # If we can't determine the next page URL, try to construct it
            if "?p=" in url:
                current_page = int(url.split("?p=")[1])
                next_page = current_page + 1
                url = url.split("?p=")[0] + f"?p={next_page}"
                page_count += 1
                # Politeness delay
                time.sleep(2)
            else:
                url = url + "?p=2"
                page_count += 1
                # Politeness delay
                time.sleep(2)
    
    logger.info(f"Crawling complete. Total books: {len(all_books)}")
    return all_books

def save_to_json(data, filename):
    """Save data to JSON file."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Data saved to {filename}")

def main():
    try:
        # Wait for a few seconds to ensure network is available
        time.sleep(5)
        
        # Crawl book data
        books = crawl_fahasa()
        
        # Save to JSON
        save_to_json(books, OUTPUT_FILE)
        
        logger.info("Crawler finished successfully")
    except Exception as e:
        logger.error(f"Crawler failed: {e}")

if __name__ == "__main__":
    main() 