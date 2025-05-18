import os
import logging
import json
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Đường dẫn tới file cấu hình 
CONFIG_FILE_PATH = os.environ.get('CRAWLER_CONFIG_PATH', os.path.join(os.path.dirname(__file__), 'crawler_config.json'))
# ID nguồn crawl từ biến môi trường
CRAWLER_SOURCE_ID = os.environ.get('CRAWLER_SOURCE_ID', 'fahasa')

# Mapping tiếng Việt sang tiếng Anh
KEY_MAPPING = {
    "mã hàng": "product_code",
    "tên nhà cung cấp": "supplier",
    "nhà cung cấp": "supplier",
    "tác giả": "author",
    "nxb": "publisher",
    "năm xb": "publish_year",
    "công ty phát hành": "distributor",
    "kích thước bao bì": "dimensions",
    "hình thức": "cover_type",
    "số trang": "page_count",
    "trọng lượng (gr)": "weight",
    "người dịch": "translator",
    "ngôn ngữ": "language"
}

# Khởi tạo CONFIG rỗng, sẽ được nạp từ file
CONFIG = {}

# Đọc cấu hình từ file
def load_config():
    """Nạp cấu hình từ file và cập nhật vào CONFIG"""
    global CONFIG
    
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                CONFIG = json.load(f)
            logger.info(f"Đã nạp cấu hình từ {CONFIG_FILE_PATH}")
        except Exception as e:
            logger.error(f"Lỗi khi nạp cấu hình từ file: {e}")
            logger.error("Khởi tạo không thành công, không có cấu hình mặc định")
            raise RuntimeError(f"Không thể đọc file cấu hình: {e}")
    else:
        raise FileNotFoundError(f"Không tìm thấy file cấu hình tại {CONFIG_FILE_PATH}")
    
    # Ghi đè một số giá trị từ .env nếu có
    CONFIG['OUTPUT_DIR'] = os.getenv('OUTPUT_DIR', CONFIG.get('OUTPUT_DIR', '/app/data'))
    CONFIG['MAX_PAGES'] = int(os.getenv('MAX_PAGES', CONFIG.get('MAX_PAGES', 1)))
    CONFIG['SCHEDULED_CRAWLING'] = os.getenv('SCHEDULED_CRAWLING', str(CONFIG.get('SCHEDULED_CRAWLING', 'false'))).lower() == 'true'
    CONFIG['SCHEDULE_TIME'] = os.getenv('SCHEDULE_TIME', CONFIG.get('SCHEDULE_TIME', '01:00'))
    CONFIG['CREATE_BACKUP_BEFORE_DELETE'] = os.getenv('CREATE_BACKUP_BEFORE_DELETE', str(CONFIG.get('CREATE_BACKUP_BEFORE_DELETE', 'false'))).lower() == 'true'
    CONFIG['INGESTION_CALLBACK_URL'] = os.getenv('INGESTION_CALLBACK_URL', CONFIG.get('INGESTION_CALLBACK_URL', ''))

    # Tạo output_files cho từng danh mục
    CONFIG['CATEGORY_OUTPUT_FILES'] = {}
    for category in CONFIG.get('ENABLED_CATEGORIES', []):
        CONFIG['CATEGORY_OUTPUT_FILES'][category] = os.path.join(
            CONFIG['OUTPUT_DIR'], 
            f"{CRAWLER_SOURCE_ID}_{category}.json"
        )

# Nạp cấu hình khi import module
load_config()

# Các hàm trợ giúp để lấy các cấu hình
def get_config(key, default=None):
    """Lấy giá trị cấu hình theo khóa"""
    return CONFIG.get(key, default)

