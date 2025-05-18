import time
from data_crawling.src.config.settings import get_config, logger
from data_crawling.src.utils.html_fetcher import get_html
from data_crawling.src.parsers.book_parser import parse_url_book, get_book_details, get_next_page_url


# 1. crawl_all_categories() lấy data từ config 
# -> lọc qua từng danh mục enabled_categories -> tạo category_url
# -> chạy crawl_books_by_category_url() 


# 2. crawl_books_by_category_url() -> nhận url từ crawl_all_categories() vd: https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html
# -> chạy get_html() -> trả về html của trang 
# -> parse_books_url() nhận vào html ở get_html -> trả về 1 mảng url của từng sách 
# -> chạy lần lượt qua từng url sách -> truỳen url vào get_book_details() -> get_book_details trả về 1 {} của sách 

def crawl_all_categories():
    """Thu thập dữ liệu sách từ Fahasa theo các danh mục đã cấu hình"""
    result = {}
    base_url = get_config('BASE_URL')
    enabled_categories = get_config('ENABLED_CATEGORIES') # mảng danh mục

    max_pages = get_config('MAX_PAGES')
    page_delay = get_config('PAGE_DELAY')
    detail_delay = get_config('DETAIL_DELAY')
    
    
    logger.info(f"Bắt đầu crawl dữ liệu từ {len(enabled_categories)} danh mục")
    
    # Crawl từng danh mục
    for category in enabled_categories:
        category_url = f"{base_url}/{category}.html"
        logger.info(f"Bắt đầu crawl danh mục: {category} từ URL: {category_url}")
        
        category_books= crawl_books_by_category_url(category_url, max_pages, page_delay, detail_delay) 
        
        # Thêm thông tin danh mục vào mỗi cuốn sách
        for book in category_books:
            if isinstance(book, dict):
                book['category'] = category
        
        result[category] = category_books
        logger.info(f"Đã crawl {len(category_books)} sách từ danh mục {category}")
        
        # Đợi giữa các danh mục để tránh quá tải server
        time.sleep(page_delay * 2)
    
    total_books = sum(len(books) for books in result.values())
    logger.info(f"Hoàn thành crawl tất cả danh mục. Tổng số sách: {total_books}")
    return result

def crawl_books_by_category_url(url, max_pages, page_delay, detail_delay):
    """Thu thập dữ liệu sách từ url của danh mục"""
    books = []
    page_count = 0
    
    while url and page_count < max_pages:
        logger.info(f"Đang crawl trang {page_count + 1}: {url}")
        html = get_html(url)
        if not html:
            logger.error(f"Không thể tải trang {page_count + 1}")
            break
        
        # trả về 1 mảng url của từng sách trong 1 danh mục
        page_books_get_url = parse_url_book(html)
        logger.info(f"Tìm thấy {len(page_books_get_url)} sách trên trang {page_count + 1}")
        
        # Thu thập chi tiết sách
        detailed_books = []
        for book in page_books_get_url:
            if "url" in book and book["url"]:
                book_details = get_book_details(book["url"])
                if book_details:
                    detailed_books.append(book_details)
                    time.sleep(detail_delay)
                else:
                    detailed_books.append(book)
            else:
                detailed_books.append(book)
        
        books.extend(detailed_books)
        
        # Lấy URL trang tiếp theo
        next_url = get_next_page_url(html, url)
        if next_url:
            url = next_url
            page_count += 1
            time.sleep(page_delay)
        else:
            break
    
    return books 