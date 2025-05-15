import time
from crawler.config.settings import (
    BASE_URL, OUTPUT_FILE, MAX_PAGES, 
    PAGE_DELAY, DETAIL_DELAY, logger
)
from crawler.utils.http import get_page
from crawler.utils.storage import save_to_json
from crawler.parsers.book_parser import (
    parse_books, get_book_details, get_next_page_url
)

def crawl_fahasa():
    """
    Hàm crawler chính để lấy sách từ Fahasa.
    
    Returns:
        list: Danh sách chi tiết các sách đã crawl
    """
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
                    time.sleep(DETAIL_DELAY)
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
            time.sleep(PAGE_DELAY)
        else:
            break
    
    logger.info(f"Hoàn tất crawl. Tổng số sách: {len(all_books)}")
    return all_books

def main():
    """Hàm main điều phối toàn bộ quá trình crawl và lưu dữ liệu."""
    try:
        # Đợi vài giây để đảm bảo mạng khả dụng
        time.sleep(5)
        
        # Crawl dữ liệu sách
        books = crawl_fahasa()
        
        # Lưu vào JSON
        save_to_json(books, OUTPUT_FILE)
        
        logger.info("Crawler hoàn thành thành công")
        return True
    except Exception as e:
        logger.error(f"Crawler thất bại: {e}")
        return False

if __name__ == "__main__":
    main() 