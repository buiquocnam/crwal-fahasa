import requests
import time
from config.settings import logger

def wait_for_api(api_url: str, max_retries: int = 30, retry_delay: int = 2) -> bool:
    """
    Chờ cho API sẵn sàng.
    
    Args:
        api_url: URL của API
        max_retries: Số lần thử lại tối đa
        retry_delay: Thời gian chờ giữa các lần thử lại (giây)
        
    Returns:
        bool: True nếu API sẵn sàng, False nếu không
    """
    retry_count = 0
    
    logger.info("Đang chờ API khả dụng...")
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"{api_url}/books", timeout=5)
            if response.status_code == 200:
                logger.info("API đã sẵn sàng!")
                return True
        except requests.RequestException:
            pass
        
        retry_count += 1
        logger.info(f"API chưa sẵn sàng. Thử lại lần {retry_count}/{max_retries}")
        time.sleep(retry_delay)
    
    logger.error("Không thể kết nối tới API")
    return False