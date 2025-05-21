import os
import requests
import concurrent.futures
from datetime import datetime
from data_crawling.src.config.settings import get_config, logger
from data_crawling.src.utils.file_utils import save_to_json, check_file_exists, create_backup
from data_crawling.src.crawlers.fahasa_crawler import crawl_books_by_category_url

def notify_ingestion():
    """Gửi thông báo đến ingestion service"""
    ingestion_url = os.environ.get("INGESTION_CALLBACK_URL")
    
    try:
        logger.info(f"Gửi thông báo đến: {ingestion_url}")
        response = requests.post(ingestion_url, timeout=5)
        
        if response.status_code == 200:
            logger.info("Thông báo thành công")
            return True
        else:
            logger.warning(f"Lỗi HTTP: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Lỗi khi gửi thông báo: {e}")
        return False

def crawl_category(category, base_url, max_pages):
    """
    Crawl một danh mục sách cụ thể theo thread riêng biệt
    
    Args:
        category: Tên danh mục
        base_url: URL cơ sở
        max_pages: Số trang tối đa cần crawl
        
    Returns:
        tuple: (category, books) - Danh mục và danh sách sách đã crawl
    """
    try:
        category_url = f"{base_url}/{category}.html"
        logger.info(f"Thread: Bắt đầu crawl danh mục: {category} từ URL: {category_url}")
        
        books = crawl_books_by_category_url(category_url, max_pages)
        
        # Thêm thông tin danh mục vào mỗi cuốn sách
        for book in books:
            if isinstance(book, dict):
                book['category'] = category
        
        logger.info(f"Thread: Đã crawl xong {len(books)} sách từ danh mục {category}")
        return category, books
    except Exception as e:
        logger.error(f"Thread: Lỗi khi crawl danh mục {category}: {e}")
        return category, []

def start_run():
    """Hàm chính xử lý toàn bộ quá trình crawl với đa luồng"""
    try:
        start_time = datetime.now()
        logger.info(f"Bắt đầu crawl vào: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
         
        # Cấu hình
        base_url = get_config('BASE_URL')
        enabled_categories = get_config('ENABLED_CATEGORIES')
        max_pages = get_config('MAX_PAGES')
        max_workers = len(enabled_categories)
        
        # Dictionary lưu kết quả
        category_books = {}
        
        # Sử dụng ThreadPoolExecutor để chạy đa luồng
        logger.info(f"Khởi tạo {max_workers} thread cho {len(enabled_categories)} danh mục")
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Tạo các nhiệm vụ crawl cho các danh mục
            future_to_category = {
                executor.submit(
                    crawl_category, 
                    category, 
                    base_url,
                    max_pages
                ): category for category in enabled_categories
            }
            
            # Xử lý kết quả khi các thread hoàn thành
            for future in concurrent.futures.as_completed(future_to_category):
                category, books = future.result()
                category_books[category] = books
                logger.info(f"Đã hoàn thành crawl danh mục: {category} với {len(books)} sách")
        
        # Lưu dữ liệu cho từng danh mục
        category_output_files = get_config('CATEGORY_OUTPUT_FILES')
        
        for category, books in category_books.items():
            output_file = category_output_files[category]
            
            # Kiểm tra và tạo backup nếu file đã tồn tại
            if check_file_exists(output_file):
                logger.info(f"File {output_file} đã tồn tại, tạo bản sao lưu...")
                backup_file = create_backup(output_file)
                if backup_file:
                    logger.info(f"Đã tạo bản sao lưu tại: {backup_file}")
            
            # Lưu dữ liệu mới (đã bật chế độ ghi đè)
            save_to_json(books, output_file, overwrite=True, create_backup_file=True)
            logger.info(f"Đã lưu {len(books)} sách từ danh mục {category} vào {output_file}")
        
        # Thông báo cho ingestion về file tổng hợp
        notify_ingestion()
        
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        logger.info(f"Hoàn thành crawl vào: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Tổng thời gian crawl: {elapsed_time:.2f} giây")
        return True
    except Exception as e:
        logger.error(f"Lỗi trong quá trình crawl: {e}")
        return False
