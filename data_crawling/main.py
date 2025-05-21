from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from data_crawling.src.config.settings import get_config, logger
from data_crawling.src.crawlers.crawler_runner import start_run
from data_crawling.src.crawlers.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Khởi động API và thiết lập crawler theo lịch"""
    logger.info("API đang khởi động")

    # Khởi động schedule nếu được cấu hình
    start_scheduler()

    yield  # Tạm dừng tại đây cho đến khi ứng dụng shutdown

    # Nếu cần xử lý khi shutdown, thêm tại đây
    logger.info("API đang tắt")

app = FastAPI(
    title="Crawler API",
)

@app.get("/")
async def root():
    """Endpoint kiểm tra trạng thái API"""
    return {
        "status": "online",
        "scheduled_crawling": get_config('SCHEDULED_CRAWLING', False),
        "schedule_time": get_config('SCHEDULE_TIME', "")
    }

@app.post("/crawl")
async def start_crawl():
    """Kích hoạt crawl thủ công"""
    start_run()
    return {"status": "started"}

if __name__ == "__main__":
    # Chạy API server
    logger.info("Khởi động API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)