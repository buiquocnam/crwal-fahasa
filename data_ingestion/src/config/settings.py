import logging
import os
import re
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Đường dẫn và API (lấy từ .env)
DATA_DIR = os.getenv("OUTPUT_DIR", "/app/data")
API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")

# Pattern kiểm tra tiếng Việt
VIETNAMESE_PATTERN = re.compile(
    r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', 
    re.IGNORECASE
)
