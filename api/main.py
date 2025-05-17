from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import time
from database import init_db
from books import router as books_router
from config import API_TITLE, API_DESCRIPTION, API_VERSION, logger

# Tạo ứng dụng FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    root_path="/api"
)

# Thêm CORS middleware để cho phép các yêu cầu từ nguồn gốc khác
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký routes
app.include_router(books_router)

@app.on_event("startup")
async def startup_event():
    """Xử lý các tác vụ khởi động ứng dụng."""
    logger.info("Ứng dụng đang khởi động...")
    
    # Thử khởi tạo database
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        if init_db():
            logger.info("Đã khởi tạo database thành công!")
            break
        else:
            retry_count += 1
            logger.warning(f"Không thể khởi tạo database. Thử lại {retry_count}/{max_retries}")
            time.sleep(3)
    
    if retry_count == max_retries:
        logger.error("Không thể khởi tạo database sau nhiều lần thử. Ứng dụng có thể không hoạt động đúng.")
    
    logger.info("Ứng dụng đã sẵn sàng!")

@app.on_event("shutdown")
async def shutdown_event():
    """Xử lý các tác vụ khi ứng dụng shutdown."""
    logger.info("Ứng dụng đang tắt...")

@app.get("/")
async def root():
    """Route chính của API."""
    return {
        "message": "API Sách Fahasa đang hoạt động!",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Xử lý các ngoại lệ không được bắt."""
    logger.error(f"Lỗi không xác định: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Đã xảy ra lỗi không xác định."}
    )



# Chạy ứng dụng nếu là file chính
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 