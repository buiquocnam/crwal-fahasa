from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from books import router as books_router
from database import wait_for_postgres
from config import API_TITLE, API_DESCRIPTION, API_VERSION

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc các domains cụ thể trong production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(books_router)

@app.on_event("startup")
async def startup_event():
    """Chạy khi API khởi động."""
    # Đợi PostgreSQL sẵn sàng
    wait_for_postgres()

@app.get("/")
async def root():
    """Endpoint gốc cung cấp thông tin API."""
    return {
        "message": "Chào mừng đến với API Sách Fahasa",
        "endpoints": [
            {"path": "/books", "description": "Lấy tất cả sách"},
            {"path": "/books/{book_id}", "description": "Lấy sách cụ thể theo ID"},
            {"path": "/books/search/title", "description": "Tìm kiếm sách theo từ khóa trong tiêu đề"},
            {"path": "/books/search/author", "description": "Tìm kiếm sách theo từ khóa trong tên tác giả"}
        ]
    } 