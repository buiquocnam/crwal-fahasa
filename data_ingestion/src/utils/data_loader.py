import os
import json
import glob
from data_ingestion.src.config.settings import (
    DATA_DIR, logger
)

def load_json_data(file_path):
    """
    Đọc dữ liệu từ file JSON.
    
    Args:
        file_path: Đường dẫn đến file JSON cần đọc
        
    Returns:
        list/dict: Dữ liệu từ file JSON hoặc None nếu thất bại
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Không tìm thấy file: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Đã đọc {len(data)} bản ghi từ {file_path}")
        return data
    except Exception as e:
        logger.error(f"Lỗi khi đọc dữ liệu JSON: {e}")
        return None

def get_all_data_files():
    """
    Lấy danh sách tất cả các file dữ liệu có thực sự tồn tại.
    
    Returns:
        list: Danh sách đường dẫn đến các file dữ liệu
    """
    files = []
    
    # Thêm các file theo danh mục
    category_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    if category_files:
        logger.info(f"Đã tìm thấy {len(category_files)} file dữ liệu theo danh mục")
        files.extend(category_files)
    
    if files:
        logger.info(f"Tổng cộng có {len(files)} file dữ liệu hợp lệ")
    else:
        logger.warning("Không tìm thấy file dữ liệu nào hợp lệ")
        
    return files 