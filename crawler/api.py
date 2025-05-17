"""
API FastAPI cho dịch vụ crawler.
"""
from fastapi import FastAPI
import uvicorn
from crawler.config.settings import get_config, logger
from crawler.crawlers.tasks import main
from crawler.crawlers.scheduler import start_scheduler

app = FastAPI(
    title="Crawler API",
    root_path="/crawler"
)
@app.on_event("startup")
async def startup_event():
    """Khởi động API và thiết lập crawler theo lịch"""
    logger.info("API đang khởi động")
    
    # Khởi động schedule nếu được cấu hình
    start_scheduler()

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
    main()
    return {"status": "started"}

if __name__ == "__main__":
    # Chạy API server
    logger.info("Khởi động API server")
    uvicorn.run("crawler.api:app", host="0.0.0.0", port=8000) 