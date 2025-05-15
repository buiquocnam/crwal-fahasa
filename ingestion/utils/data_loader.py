import os
import json
import glob
from ingestion.config.settings import (
    DATA_DIR, COMBINED_DATA_FILE, logger
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
    
    # Thêm file tổng hợp nếu có
    if os.path.exists(COMBINED_DATA_FILE):
        logger.info(f"Đã tìm thấy file dữ liệu tổng hợp: {COMBINED_DATA_FILE}")
        files.append(COMBINED_DATA_FILE)
    
    # Thêm các file theo danh mục
    category_files = glob.glob(os.path.join(DATA_DIR, "fahasa_*.json"))
    if category_files:
        logger.info(f"Đã tìm thấy {len(category_files)} file dữ liệu theo danh mục")
        files.extend(category_files)
    
    # Kiểm tra xác nhận tất cả các files
    for file in list(files):  # Sử dụng một bản sao để có thể xóa trong khi lặp
        if not os.path.exists(file):
            logger.warning(f"File {file} không tồn tại, bỏ qua")
            files.remove(file)
        elif os.path.getsize(file) == 0:
            logger.warning(f"File {file} rỗng, bỏ qua")
            files.remove(file)
    
    if files:
        logger.info(f"Tổng cộng có {len(files)} file dữ liệu hợp lệ")
    else:
        logger.warning("Không tìm thấy file dữ liệu nào hợp lệ")
        
    return files 