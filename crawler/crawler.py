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
MAX_PAGES = 1  # Giới hạn 5 trang để test nhanh hơn

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

def get_book_details(book_url):
    """Truy cập trang chi tiết sách và lấy thông tin."""
    logger.info(f"Lấy thông tin chi tiết từ: {book_url}")
    
    html = get_page(book_url)
    if not html:
        logger.error(f"Không thể tải trang chi tiết sách: {book_url}")
        return None
        
    soup = BeautifulSoup(html, 'lxml')
    details = {}
    
    try:
        # Lấy tiêu đề sách
        title_element = soup.select_one("div.product-essential h1") 
        if title_element:
            details["title"] = title_element.get_text(strip=True)
            # logger.info(f"Tiêu đề: {details['title']}")
        
        # Lấy mô tả sách
        description_element = soup.select_one("div.std")
        if description_element:
            details["description"] = description_element.get_text(strip=True)
            # logger.info(f"Mô tả: {details['description'][:50]}...")
        
        # Lấy giá bán
        price_element = soup.select_one("div.price-box p.special-price span.price")
        if price_element:
            details["price"] = price_element.get_text(strip=True)
            # logger.info(f"Giá: {details['price']}")
        
        # Lấy giá gốc (nếu có)
        original_price_element = soup.select_one("div.price-box p.old-price span.price")
        if original_price_element:
            details["original_price"] = original_price_element.get_text(strip=True)
            # logger.info(f"Giá gốc: {details['original_price']}")
        
        # Lấy phần trăm giảm giá (nếu có)
        discount_element = soup.select_one("span.discount-percent")
        if discount_element:
            details["discount"] = discount_element.get_text(strip=True)
            # logger.info(f"Giảm giá: {details['discount']}")
        
        # Lấy URL hình ảnh
        image_element =  soup.select_one("meta[property='og:image']")
        if image_element:
                details["image_url"] = image_element.get("content")
        
        # Lấy thông số kỹ thuật từ bảng thông tin sách
        info_table = soup.select_one("table.data-table")
        if info_table:
            rows = info_table.select("tr") or info_table.select("tbody tr")
            for row in rows:
                cells = row.select("th, td") or row.select("td")
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    
                    # Chuyển đổi key sang tiếng Anh để dễ sử dụng
                    key_mapping = {
                        "mã hàng": "product_code",
                        "tên nhà cung cấp": "supplier",
                        "nhà cung cấp": "supplier",
                        "tác giả": "author",
                        "nxb": "publisher",
                        "năm xb": "publish_year",
                        "công ty phát hành": "distributor",
                        "kích thước bao bì": "dimensions",
                        "hình thức": "cover_type",
                        "số trang": "page_count",
                        "trọng lượng (gr)": "weight",
                    }
                    # Kiểm tra xem key có trong mapping không, nếu không thì kiểm tra thêm
                    normalized_key = key_mapping.get(key, key.replace(" ", "_"))
                    
                    details[normalized_key] = value
                    # logger.info(f"Thông tin: {key} -> {normalized_key} = {value}")
        # Đảm bảo có URL trong chi tiết
        details["url"] = book_url
        
        # Kiểm tra kết quả
        if len(details) > 1:  # Luôn có ít nhất URL
            logger.info(f"Lấy được {len(details)} thuộc tính từ trang chi tiết")
        else:
            logger.warning(f"Lấy được rất ít thông tin từ trang chi tiết: {book_url}")
            
        return details
            
    except Exception as e:
        logger.error(f"Lỗi khi phân tích trang chi tiết: {e}")
        return {"url": book_url, "error": str(e)}

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
     
            # Xây dựng dữ liệu sách
            book_data = {
                "title": title,
                "url": book_url,
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
        
        # Lấy thông tin chi tiết cho từng sách
        detailed_books = []
        for book in books:
            if "url" in book and book["url"]:
                book_details = get_book_details(book["url"])
                if book_details:
                    detailed_books.append(book_details)
                    # Delay lịch sự giữa các yêu cầu
                    time.sleep(1)
                else:
                    # Nếu không lấy được chi tiết, vẫn giữ thông tin cơ bản
                    detailed_books.append(book)
            else:
                detailed_books.append(book)
        
        all_books.extend(detailed_books)
        
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