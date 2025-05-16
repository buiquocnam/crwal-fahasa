from fastapi import FastAPI, BackgroundTasks
import logging
import os
from datetime import datetime
from ingestion.main import main as run_ingestion
from pydantic import BaseModel

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ingestion API")

class CrawlerCallback(BaseModel):
    source_id: str
    output_file: str

# Trạng thái đơn giản
last_run = {"timestamp": None, "success": None}

def process_data():
    """Xử lý dữ liệu trong background"""
    try:
        logger.info("Bắt đầu xử lý dữ liệu...")
        success = run_ingestion()
        last_run["timestamp"] = datetime.now().isoformat()
        last_run["success"] = success
        logger.info(f"Xử lý dữ liệu hoàn tất: {'thành công' if success else 'thất bại'}")
    except Exception as e:
        logger.error(f"Lỗi xử lý: {e}")
        last_run["success"] = False

@app.get("/", status_code=200)
async def health_check():
    return {"status": "online"}

@app.post("/trigger")
async def trigger_ingestion(callback: CrawlerCallback, background_tasks: BackgroundTasks):
    """Endpoint nhận callback từ crawler"""
    logger.info(f"Nhận callback từ nguồn: {callback.source_id}")
    
    # Kiểm tra file dữ liệu
    if not os.path.exists(callback.output_file):
        logger.error(f"File không tồn tại: {callback.output_file}")
        return {"success": False, "error": "File không tồn tại"}
    
    # Xử lý dữ liệu trong background
    background_tasks.add_task(process_data)
    return {"success": True}

@app.get("/status")
async def get_status():
    """Lấy trạng thái xử lý cuối cùng"""
    return last_run

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ingestion.api:app", host="0.0.0.0", port=8000) 