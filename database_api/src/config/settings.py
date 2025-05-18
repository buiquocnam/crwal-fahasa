import os
import logging
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cấu hình database từ biến môi trường
DB_HOST = os.getenv("DB_HOST", "postgres")  # Sử dụng tên service trong docker-compose
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fahasa_db")
DB_USER = os.getenv("DB_USER", "fahasa")
DB_PASS = os.getenv("DB_PASS", "fahasa123")

# Tạo chuỗi kết nối SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cấu hình API
API_TITLE = "API Sách Fahasa"
API_DESCRIPTION = "API để truy vấn dữ liệu sách từ Fahasa"
API_VERSION = "1.0.0"

# Cấu hình phân trang
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", 10))
MAX_LIMIT = int(os.getenv("MAX_LIMIT", 1000))

