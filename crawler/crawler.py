import requests
import json
import os
import time
from bs4 import BeautifulSoup
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Các hằng số
BASE_URL = "https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html"
OUTPUT_DIR = "/app/data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fahasa_data.json")
MAX_PAGES = 5  # Giới hạn 5 trang để test nhanh hơn

def get_page(url):
    """Lấy nội dung trang từ Fahasa với cơ chế thử lại."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }
    
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.encoding = 'utf-8'  # Đảm bảo encoding đúng cho tiếng Việt
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            retry_count += 1
            logger.warning(f"Yêu cầu thất bại ({retry_count}/{max_retries}): {e}")
            time.sleep(2)  # Đợi trước khi thử lại
    
    logger.error(f"Không thể tải {url} sau {max_retries} lần thử")
    return None

def parse_books(html):
    """Phân tích HTML để trích xuất thông tin sách từ website Fahasa."""
    soup = BeautifulSoup(html, 'lxml')
    books = []
    
    logger.info("Đang phân tích cấu trúc trang...")
    
    # Tìm container chứa sản phẩm
    products_container = soup.select_one("ul#products_grid.products-grid")
    if not products_container:
        logger.warning("Không tìm thấy khung chứa sản phẩm")
        return books
    
    # Tìm tất cả các mục sách (thẻ li là con trực tiếp của products grid)
    book_elements = products_container.find_all("li", recursive=False)
    
    logger.info(f"Đã tìm thấy {len(book_elements)} sách trên trang")
    
    for book in book_elements:
        try:
            # Trích xuất tiêu đề
            title_element = book.select_one("h2.product-name-no-ellipsis a") or book.select_one("a.product-image")
                
            if not title_element:
                logger.warning("Không tìm thấy tiêu đề, bỏ qua sách này")
                continue
            
            # Lấy text tiêu đề, làm sạch các phần tử phụ
            title = title_element.get_text(strip=True)
            
            # Lấy URL sách
            book_url = title_element.get('href', '')
            if book_url and not book_url.startswith('http'):
                book_url = f"https://www.fahasa.com{book_url}" if book_url.startswith('/') else f"https://www.fahasa.com/{book_url}"
            
            # Trích xuất tác giả
            author_element = book.select_one("div.product-author span")
            author = author_element.get_text(strip=True) if author_element else None
            
            # Trích xuất giá
            special_price_element = book.select_one("p.special-price span.price")
            if special_price_element:
                price = special_price_element.get_text(strip=True)
            else:
                price_element = book.select_one("span.price")
                price = price_element.get_text(strip=True) if price_element else "N/A"
            
            # Trích xuất giá gốc
            old_price_element = book.select_one("p.old-price span.price")
            old_price = old_price_element.get_text(strip=True) if old_price_element else None
            
            # Trích xuất phần trăm giảm giá
            discount_element = book.select_one("span.discount-percent")
            discount = discount_element.get_text(strip=True) if discount_element else None
            
            # Trích xuất URL hình ảnh
            img_element = book.select_one("span.product-image img.lazyload")
            img_url = None
            if img_element:
                img_url = img_element.get('data-src') or img_element.get('src')
            
            # Xây dựng dữ liệu sách
            book_data = {
                "title": title,
                "author": author,
                "price": price,
                "original_price": old_price,
                "discount": discount,
                "url": book_url,
                "image_url": img_url
            }
            
            books.append(book_data)
            
        except Exception as e:
            logger.warning(f"Lỗi khi phân tích sách: {e}")
    
    return books

def get_next_page_url(html, current_url):
    """Trích xuất URL cho trang tiếp theo."""
    soup = BeautifulSoup(html, 'lxml')
    
    # Tìm phần phân trang
    pagination = soup.select_one("div.pages")
    if not pagination:
        return None
    
    # Tìm nút next
    next_page_link = soup.find("a", onclick=lambda x: x and "catalog_ajax.Page_change('next')" in x)
    if next_page_link:
        # Lấy số trang hiện tại từ các nguồn có thể
        current_page_element = soup.select_one("li.current a")
        if current_page_element:
            try:
                current_page = int(current_page_element.get_text(strip=True))
                next_page = current_page + 1
                
                # Tạo URL trang tiếp theo
                base_url = current_url.split('?')[0] if '?' in current_url else current_url
                if not base_url.endswith('.html'):
                    base_url = f"{base_url}.html"
                return f"{base_url}?p={next_page}"
            except (ValueError, TypeError) as e:
                logger.warning(f"Lỗi phân tích phân trang: {e}")
                return None
    
    return None

def crawl_fahasa():
    """Hàm crawler chính để lấy sách từ Fahasa."""
    all_books = []
    url = BASE_URL
    page_count = 0
    
    logger.info("Bắt đầu crawler Fahasa")
    
    while url and page_count < MAX_PAGES:
        logger.info(f"Đang crawl trang {page_count + 1}: {url}")
        html = get_page(url)
        if not html:
            logger.error(f"Không thể lấy trang {page_count + 1}")
            break
        
        books = parse_books(html)
        logger.info(f"Đã tìm thấy {len(books)} sách trên trang {page_count + 1}")
        all_books.extend(books)
        
        # Lấy URL trang tiếp theo
        next_url = get_next_page_url(html, url)
        if next_url:
            url = next_url
            page_count += 1
            # Delay lịch sự
            time.sleep(2)
        else:
            # Nếu không xác định được URL trang tiếp theo, thử tạo URL
            if "?p=" in url:
                current_page = int(url.split("?p=")[1])
                next_page = current_page + 1
                url = url.split("?p=")[0] + f"?p={next_page}"
                page_count += 1
                time.sleep(2)
            else:
                url = url + "?p=2"
                page_count += 1
                time.sleep(2)
    
    logger.info(f"Hoàn tất crawl. Tổng số sách: {len(all_books)}")
    return all_books

def save_to_json(data, filename):
    """Lưu dữ liệu vào file JSON."""
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Đã lưu dữ liệu vào {filename}")

def main():
    try:
        # Đợi vài giây để đảm bảo mạng khả dụng
        time.sleep(5)
        
        # Crawl dữ liệu sách
        books = crawl_fahasa()
        
        # Lưu vào JSON
        save_to_json(books, OUTPUT_FILE)
        
        logger.info("Crawler hoàn thành thành công")
    except Exception as e:
        logger.error(f"Crawler thất bại: {e}")

if __name__ == "__main__":
    main() 