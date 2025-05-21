from fastapi import FastAPI
from datetime import datetime
from data_ingestion.src.ingestion import run_ingestion
from data_ingestion.src.config.settings import logger

app = FastAPI(title="Ingestion API")

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
async def trigger_ingestion():
    """Endpoint nhận callback từ crawler"""
    process_data()
    return {"success": True}

@app.get("/status")
async def get_status():
    """Lấy trạng thái xử lý cuối cùng"""
    return last_run
