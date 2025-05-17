import os
import json
import shutil
from datetime import datetime
from crawler.config.settings import logger

def check_file_exists(filename):
    """
    Kiểm tra file có tồn tại không.
    
    Args:
        filename: Đường dẫn file cần kiểm tra
        
    Returns:
        bool: True nếu file tồn tại, False nếu không
    """
    return os.path.exists(filename)

def create_backup(filename):
    """
    Tạo bản sao lưu của file hiện tại.
    
    Args:
        filename: Đường dẫn file cần sao lưu
        
    Returns:
        str: Đường dẫn đến file sao lưu
    """
    if not check_file_exists(filename):
        return None
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{filename}.{timestamp}.bak"
    
    try:
        shutil.copy2(filename, backup_filename)
        logger.info(f"Đã tạo bản sao lưu tại {backup_filename}")
        return backup_filename
    except Exception as e:
        logger.error(f"Lỗi khi tạo bản sao lưu {filename}: {e}")
        return None

def save_to_json(data, filename, overwrite=True, create_backup_file=False):
    """
    Lưu dữ liệu vào file JSON.
    
    Args:
        data: Dữ liệu cần lưu
        filename: Đường dẫn file JSON đích
        overwrite: Có ghi đè file hiện tại không
        create_backup_file: Có tạo bản sao lưu trước khi ghi đè không
        
    Returns:
        bool: True nếu lưu thành công, False nếu không
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