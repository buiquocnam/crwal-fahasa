import os
import requests
from datetime import datetime
from crawler.config.settings import get_config, logger
from crawler.utils.storage import save_to_json, check_file_exists, create_backup
from crawler.crawlers.fahasa_crawler import crawl_data

# Biến theo dõi trạng thái
crawler_running = False

def notify_ingestion():
    """Gửi thông báo đến ingestion service"""
    ingestion_url = os.environ.get("INGESTION_CALLBACK_URL", "http://ingestion:8000/trigger")
    
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


def main():
    """Hàm chính xử lý toàn bộ quá trình crawl"""
    global crawler_running
    
    if crawler_running:
        logger.info("Đã có một tiến trình crawler đang chạy, bỏ qua")
        return False
        
    try:
        crawler_running = True
        logger.info(f"Bắt đầu crawl vào: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
         
        # Thu thập dữ liệu
        category_books = crawl_data()
        all_books = []
        
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
            all_books.extend(books)
        
        # Thông báo cho ingestion về file tổng hợp
        notify_ingestion()
        
        logger.info(f"Hoàn thành crawl vào: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    except Exception as e:
        logger.error(f"Lỗi trong quá trình crawl: {e}")
        return False
    finally:
        crawler_running = False
