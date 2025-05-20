import requests
import time
from config.settings import logger

def wait_for_api(api_url: str, max_retries: int = 30, retry_delay: int = 2) -> bool:
    """
    Wait for API to be ready.
    
    Args:
        api_url: API URL
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        bool: True if API is ready, False otherwise
    """
    retry_count = 0
    
    logger.info("Waiting for API to be available...")
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"{api_url}/books", timeout=5)
            if response.status_code == 200:
                logger.info("API is available!")
                return True
        except requests.RequestException:
            pass
        
        retry_count += 1
        logger.info(f"API not available yet. Retry {retry_count}/{max_retries}")
        time.sleep(retry_delay)
    
    logger.error("Failed to connect to API")
    return False 