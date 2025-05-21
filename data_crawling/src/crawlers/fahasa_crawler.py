import time
from data_crawling.src.config.settings import get_config, logger
from data_crawling.src.utils.html_fetcher import get_html
from data_crawling.src.parsers.book_parser import parse_url_book, get_book_details, get_next_page_url

def crawl_books_by_category_url(url, max_pages):
    """
    Thu thập dữ liệu sách từ url của danh mục
    
    Args:
        url: URL của danh mục
        max_pages: Số trang tối đa cần crawl
        page_delay: Thời gian chờ giữa các trang
        detail_delay: Thời gian chờ giữa chi tiết sách
    
    Returns:
        list: Danh sách sách đã crawl
    """
    books = []
    page_count = 0
    
    while url and page_count < max_pages:
        logger.info(f"Đang crawl trang {page_count + 1}: {url}")
        html = get_html(url)
        if not html:
            logger.error(f"Không thể tải trang {page_count + 1}")
            break
        
        # trả về 1 mảng url của từng sách trong 1 danh mục
        page_books_get_url = parse_url_book(html)
        logger.info(f"Tìm thấy {len(page_books_get_url)} sách trên trang {page_count + 1}")
        
        # Thu thập chi tiết sách
        detailed_books = []
        for book in page_books_get_url:
            if "url" in book and book["url"]:
                book_details = get_book_details(book["url"])
                if book_details:
                    detailed_books.append(book_details)
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
        else:
            break
    
    return books 