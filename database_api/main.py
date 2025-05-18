from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import time
from database_api.src.database.init_db import init_db
from database_api.src.routers.book_router import router as books_router
from database_api.src.config.settings import API_TITLE, API_DESCRIPTION, API_VERSION, logger

# Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Ứng dụng đang khởi động...")
    
    retry_count = 0
    max_retries = 5
    retry_interval = 3

    while retry_count < max_retries:
        try:
            if init_db():
                logger.info("Đã khởi tạo database thành công!")
                break
            else:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"Không thể khởi tạo database. Thử lại {retry_count}/{max_retries}")
                    time.sleep(retry_interval)
                else:
                    logger.error("Không thể khởi tạo database sau nhiều lần thử. Ứng dụng có thể không hoạt động đúng.")
        except Exception as e:
            retry_count += 1
            logger.error(f"Lỗi khi khởi tạo database: {e}")
            if retry_count < max_retries:
                time.sleep(retry_interval)
            else:
                logger.error("Không thể khởi tạo database sau nhiều lần thử. Ứng dụng có thể không hoạt động đúng.")

    logger.info("Ứng dụng đã sẵn sàng!")
    yield
    logger.info("Ứng dụng đang tắt...")

# Tạo ứng dụng FastAPI với lifespan
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
    root_path="/api"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(books_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "API Sách Fahasa đang hoạt động!",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Run server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)