from bs4 import BeautifulSoup
import re
from crawler.config.settings import KEY_MAPPING, logger
from crawler.utils.http import get_page

def parse_books(html):
    """
    Phân tích HTML để trích xuất thông tin sách từ website Fahasa.
    
    Args:
        html: Nội dung HTML của trang danh sách sách
        
    Returns:
        list: Danh sách thông tin cơ bản các sách
    """
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

def get_book_details(book_url):
    """
    Truy cập trang chi tiết sách và lấy thông tin.
    
    Args:
        book_url: URL trang chi tiết sách
        
    Returns:
        dict: Thông tin chi tiết sách
    """
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
        
        # Lấy mô tả sách
        description_element = soup.select_one("div.std")
        if description_element:
            details["description"] = description_element.get_text(strip=True)
        
        # Lấy giá bán
        price_element = soup.select_one("div.price-box p.special-price span.price")
        if price_element:
            details["price"] = price_element.get_text(strip=True)
        
        # Lấy giá gốc (nếu có)
        original_price_element = soup.select_one("div.price-box p.old-price span.price")
        if original_price_element:
            details["original_price"] = original_price_element.get_text(strip=True)
        
        # Lấy phần trăm giảm giá (nếu có)
        discount_element = soup.select_one("span.discount-percent")
        if discount_element:
            details["discount"] = discount_element.get_text(strip=True)
        
        # Lấy URL hình ảnh
        image_element = soup.select_one("meta[property='og:image']")
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
                    normalized_key = KEY_MAPPING.get(key, key.replace(" ", "_"))
                    details[normalized_key] = value
                    
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


def get_next_page_url(html, current_url):
    """
    Trích xuất URL cho trang tiếp theo.
    
    Args:
        html: Nội dung HTML trang hiện tại
        current_url: URL trang hiện tại
        
    Returns:
        str: URL trang tiếp theo hoặc None nếu không tìm thấy
    """
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
    
    # Thử tạo URL trang tiếp theo từ URL hiện tại
    if "?p=" in current_url:
        try:
            current_page = int(current_url.split("?p=")[1])
            next_page = current_page + 1
            return current_url.split("?p=")[0] + f"?p={next_page}"
        except (ValueError, IndexError):
            pass
    else:
        return current_url + "?p=2"
        
    return None 