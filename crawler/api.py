"""
API FastAPI cho dịch vụ crawler.
"""
from fastapi import FastAPI, BackgroundTasks
import uvicorn
from crawler.config.settings import get_config, logger
from crawler.crawlers.tasks import background_crawl
from crawler.crawlers.scheduler import start_scheduler

app = FastAPI(title="Crawler API")

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
@app.get("/crawl")
async def start_crawl(background_tasks: BackgroundTasks):
    """Kích hoạt crawl thủ công"""
    background_tasks.add_task(background_crawl)
    return {"status": "started"}

if __name__ == "__main__":
    # Chạy API server
    logger.info("Khởi động API server")
    uvicorn.run("crawler.api:app", host="0.0.0.0", port=8000) 