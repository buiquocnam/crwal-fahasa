import os
import logging
import re

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Đường dẫn và API
DATA_DIR = "/app/data"
COMBINED_DATA_FILE = os.path.join(DATA_DIR, "fahasa_data.json")  # File tổng hợp
API_BASE_URL = "http://api:8000"  # URL của API service trong Docker

# Pattern kiểm tra tiếng Việt
VIETNAMESE_PATTERN = re.compile(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', re.IGNORECASE) 