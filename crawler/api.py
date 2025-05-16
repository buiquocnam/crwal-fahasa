from fastapi import FastAPI, BackgroundTasks
import threading
import schedule
import time
import os
import requests
import uvicorn
from datetime import datetime
from crawler.config.settings import get_config, logger
from crawler.utils.http import get_page
from crawler.utils.storage import save_to_json
from crawler.parsers.book_parser import parse_books, get_book_details, get_next_page_url

app = FastAPI(title="Crawler API")

# Biến theo dõi trạng thái
crawler_running = False
stop_scheduler = False

def notify_ingestion(output_file):
    """Gửi thông báo đến ingestion service"""
    source_id = os.environ.get('CRAWLER_SOURCE_ID', 'fahasa')
    ingestion_url = os.environ.get("INGESTION_CALLBACK_URL", "http://ingestion:8000/trigger")
    
    try:
        payload = {
            "source_id": source_id,
            "output_file": output_file
        }
        
        logger.info(f"Gửi thông báo đến: {ingestion_url}")
        response = requests.post(ingestion_url, json=payload, timeout=5)
        
        if response.status_code == 200:
            logger.info("Thông báo thành công")
            return True
        else:
            logger.warning(f"Lỗi HTTP: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Lỗi khi gửi thông báo: {e}")
        return False

def crawl_data():
    """Thu thập dữ liệu sách từ Fahasa"""
    all_books = []
    url = get_config('BASE_URL')
    page_count = 0
    max_pages = get_config('MAX_PAGES')
    page_delay = get_config('PAGE_DELAY')
    detail_delay = get_config('DETAIL_DELAY')
    
    logger.info("Bắt đầu crawl dữ liệu")
    
    while url and page_count < max_pages:
        logger.info(f"Đang crawl trang {page_count + 1}: {url}")
        html = get_page(url)
        if not html:
            logger.error(f"Không thể tải trang {page_count + 1}")
            break
        
        books = parse_books(html)
        logger.info(f"Tìm thấy {len(books)} sách trên trang {page_count + 1}")
        
        # Thu thập chi tiết sách
        detailed_books = []
        for book in books:
            if "url" in book and book["url"]:
                book_details = get_book_details(book["url"])
                if book_details:
                    detailed_books.append(book_details)
                    time.sleep(detail_delay)
                else:
                    detailed_books.append(book)
            else:
                detailed_books.append(book)
        
        all_books.extend(detailed_books)
        
        # Lấy URL trang tiếp theo
        next_url = get_next_page_url(html, url)
        if next_url:
            url = next_url
            page_count += 1
            time.sleep(page_delay)
        else:
            break
    
    logger.info(f"Hoàn thành crawl. Tổng số sách: {len(all_books)}")
    return all_books

def crawler_task():
    """Hàm chính xử lý toàn bộ quá trình crawl"""
    global crawler_running
    
    if crawler_running:
        logger.info("Đã có một tiến trình crawler đang chạy, bỏ qua")
        return False
        
    try:
        crawler_running = True
        logger.info(f"Bắt đầu crawl vào: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Thu thập dữ liệu
        books = crawl_data()
        
        # Lưu dữ liệu
        output_file = get_config('OUTPUT_FILE')
        save_to_json(books, output_file)
        logger.info(f"Đã lưu {len(books)} sách vào {output_file}")
        
        # Thông báo cho ingestion
        notify_ingestion(output_file)
        
        return True
    except Exception as e:
        logger.error(f"Lỗi trong quá trình crawl: {e}")
        return False
    finally:
        crawler_running = False

def run_scheduler():
    """Chạy schedule crawler theo cấu hình"""
    schedule_time = get_config('SCHEDULE_TIME')
    logger.info(f"Đã khởi động scheduler, sẽ chạy crawler vào lúc {schedule_time} hàng ngày")
    
    # Thiết lập schedule
    schedule.every().day.at(schedule_time).do(crawler_task)
    
    # Chạy schedule loop
    while not stop_scheduler:
        schedule.run_pending()
        time.sleep(60)  # Kiểm tra mỗi phút

def start_scheduler():
    """Khởi động scheduler trong thread riêng nếu được cấu hình"""
    if get_config('SCHEDULED_CRAWLING', False):
        logger.info("Khởi động chế độ lập lịch theo cấu hình")
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
    else:
        logger.info("Chế độ lập lịch không được bật trong cấu hình")

def background_crawl():
    """Chạy crawler trong background thread"""
    try:
        crawler_task()
    except Exception as e:
        logger.error(f"Lỗi: {e}")

@app.on_event("startup")
async def startup_event():
    """Khởi động API và thiết lập crawler theo lịch"""
    logger.info("API đang khởi động")
    
    # Khởi động schedule nếu được cấu hình
    start_scheduler()

@app.get("/")
async def root():
    return {
        "status": "online",
        "scheduled_crawling": get_config('SCHEDULED_CRAWLING', False),
        "schedule_time": get_config('SCHEDULE_TIME', "")
    }

@app.post("/crawl")
@app.get("/crawl")
async def start_crawl(background_tasks: BackgroundTasks):
    """Kích hoạt crawl thủ công"""
    background_tasks.add_task(background_crawl)
    return {"status": "started"}

if __name__ == "__main__":
    # Chạy API server
    logger.info("Khởi động API server")
    uvicorn.run("crawler.api:app", host="0.0.0.0", port=8000) 