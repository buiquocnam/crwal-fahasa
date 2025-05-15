import os
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Các hằng số
BASE_URL = "https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html"
OUTPUT_DIR = "/app/data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fahasa_data.json")
MAX_PAGES = 1  # Giới hạn số trang để crawl

# Cấu hình HTTP Request
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive"
}

# Mapping tiếng Việt sang tiếng Anh cho các trường thông tin
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

# Cấu hình thời gian chờ giữa các request
REQUEST_TIMEOUT = 15  # Thời gian tối đa cho mỗi request (giây)
RETRY_DELAY = 2       # Thời gian chờ giữa các lần thử lại (giây)
PAGE_DELAY = 2        # Thời gian chờ giữa các trang (giây)
DETAIL_DELAY = 1      # Thời gian chờ giữa các request chi tiết sách (giây)
MAX_RETRIES = 3       # Số lần thử lại tối đa khi request thất bại 