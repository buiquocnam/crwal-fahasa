import os
import json
from crawler.config.settings import logger

def save_to_json(data, filename):
    """
    Lưu dữ liệu vào file JSON.
    
    Args:
        data: Dữ liệu cần lưu
        filename: Đường dẫn file JSON đích
    """
    try:
        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Đã lưu dữ liệu vào {filename}")
        return True
    except Exception as e:
        logger.error(f"Lỗi khi lưu dữ liệu vào file {filename}: {e}")
        return False 