import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cấu hình Database
DB_HOST = "postgres"
DB_NAME = "fahasa_db"  # Đảm bảo tên này trùng với POSTGRES_DB trong docker-compose
DB_USER = "fahasa"     # Đảm bảo tên này trùng với POSTGRES_USER trong docker-compose
DB_PASSWORD = "fahasa123"  # Đảm bảo mật khẩu này trùng với POSTGRES_PASSWORD trong docker-compose
DB_PORT = 5432

# Cấu hình API
API_TITLE = "API Sách Fahasa"
API_DESCRIPTION = "API để truy vấn dữ liệu sách từ Fahasa"
API_VERSION = "1.0.0"

# Cấu hình phân trang
DEFAULT_LIMIT = 20
MAX_LIMIT = 100 