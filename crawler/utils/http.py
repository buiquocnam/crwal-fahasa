import requests
import time
from crawler.config.settings import REQUEST_HEADERS, REQUEST_TIMEOUT, RETRY_DELAY, MAX_RETRIES, logger

def get_page(url):
    """
    Lấy nội dung trang từ Fahasa với cơ chế thử lại.
    
    Args:
        url: URL cần crawl
        
    Returns:
        str: HTML content hoặc None nếu thất bại
    """
    retry_count = 0
    
    while retry_count < MAX_RETRIES:
        try:
            response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
            response.encoding = 'utf-8'  # Đảm bảo encoding đúng cho tiếng Việt
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            retry_count += 1
            logger.warning(f"Yêu cầu thất bại ({retry_count}/{MAX_RETRIES}): {e}")
            time.sleep(RETRY_DELAY)  # Đợi trước khi thử lại
    
    logger.error(f"Không thể tải {url} sau {MAX_RETRIES} lần thử")
    return None 