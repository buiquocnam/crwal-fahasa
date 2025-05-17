import requests
import time
from crawler.config.settings import get_config, logger

def get_html(url):
    """
    Lấy nội dung trang từ Fahasa với cơ chế thử lại.
    
    Args:
        url: URL cần crawl
        
    Returns:
        str: HTML content hoặc None nếu thất bại
    """
    retry_count = 0
    max_retries = get_config('MAX_RETRIES')
    headers = get_config('REQUEST_HEADERS')
    timeout = get_config('REQUEST_TIMEOUT')
    retry_delay = get_config('RETRY_DELAY')
    
    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.encoding = 'utf-8'  # Đảm bảo encoding đúng cho tiếng Việt
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            retry_count += 1
            logger.warning(f"Yêu cầu thất bại ({retry_count}/{max_retries}): {e}")
            time.sleep(retry_delay)  # Đợi trước khi thử lại
    
    logger.error(f"Không thể tải {url} sau {max_retries} lần thử")
    return None 