import os
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Giới hạn tìm kiếm
DEFAULT_LIMIT = 10
MAX_LIMIT = 100 

# Cấu hình database
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "books_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# Tạo chuỗi kết nối SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cấu hình API
API_TITLE = "API Sách Fahasa"
API_DESCRIPTION = "API để truy vấn dữ liệu sách từ Fahasa"
API_VERSION = "1.0.0" 