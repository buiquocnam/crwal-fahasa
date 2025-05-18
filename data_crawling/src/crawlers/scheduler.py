"""
Module chứa các hàm lập lịch cho crawler.
"""
import threading
import schedule
import time
from data_crawling.src.config.settings import get_config, logger
from data_crawling.src.crawlers.crawler_runner import start_run

# Biến theo dõi trạng thái scheduler
stop_scheduler = False

def run_scheduler():
    """Chạy schedule crawler theo cấu hình"""
    global stop_scheduler
    
    schedule_time = get_config('SCHEDULE_TIME')
    logger.info(f"Đã khởi động scheduler, sẽ chạy crawler vào lúc {schedule_time} hàng ngày")
    
    # Thiết lập schedule
    schedule.every().day.at(schedule_time).do(start_run)
    
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