import json
import requests
from ingestion.config.settings import API_BASE_URL, logger

def import_books_batch(books):
    """
    Nhập nhiều sách cùng lúc thông qua API batch.
    
    Args:
        books: Danh sách sách cần nhập
        
    Returns:
        dict: Kết quả nhập dữ liệu {success_count, failed_count, failed_items}
    """
    if not books:
        logger.warning("Không có sách nào để nhập qua batch")
        return {"success_count": 0, "failed_count": 0, "failed_items": []}
    
    try:
        logger.info(f"Đang nhập {len(books)} sách qua API endpoint batch...")
        response = requests.post(f"{API_BASE_URL}/books/batch", json=books)
        
        if response.status_code in [200, 201]:
            result = response.json()
            logger.info(f"Đã nhập thành công {result.get('success_count')} sách vào database")
            
            if result.get('failed_count', 0) > 0:
                logger.warning(f"Có {result.get('failed_count')} sách không thể nhập")
                for failed in result.get('failed_items', []):
                    logger.warning(f"- Sách '{failed.get('title')}': {failed.get('error')}")
            
            return result
        else:
            logger.error(f"Lỗi khi nhập sách qua API batch: {response.status_code} - {response.text}")
            return {"success_count": 0, "failed_count": len(books), "failed_items": []}
    except Exception as e:
        logger.error(f"Lỗi khi sử dụng endpoint batch: {e}")
        return {"success_count": 0, "failed_count": len(books), "failed_items": []}

def delete_all_books():
    """
    Xóa tất cả sách trong database thông qua API.
    
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
        int: Số lượng sách đã xóa
    """
    try:
        logger.info("Đang xóa tất cả sách từ database...")
        response = requests.delete(f"{API_BASE_URL}/books/deleteAll")
        
        if response.status_code == 200:
            result = response.json()
            count = result.get("count", 0)
            logger.info(f"Đã xóa thành công {count} sách từ database")
            return True, count
        else:
            logger.error(f"Lỗi khi xóa sách: {response.status_code} - {response.text}")
            return False, 0
    except Exception as e:
        logger.error(f"Lỗi khi gọi API xóa sách: {e}")
        return False, 0