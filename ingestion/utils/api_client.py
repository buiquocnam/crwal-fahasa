import json
import requests
from ingestion.config.settings import API_BASE_URL, logger

def import_book_via_api(book):
    """
    Nhập một cuốn sách thông qua API.
    
    Args:
        book: Thông tin sách cần nhập
        
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    try:
        # In ra thông tin sách để debug
        logger.info(f"Thêm sách: {book.get('title')}, Dữ liệu: {json.dumps(book, ensure_ascii=False)}")
        
        # Sử dụng endpoint POST /books 
        response = requests.post(f"{API_BASE_URL}/books", json=book)
        if response.status_code in [200, 201]:
            return True
        else:
            logger.error(f"Lỗi khi thêm sách qua API: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Lỗi khi gửi request thêm sách: {e}")
        return False

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

def import_books_one_by_one(books):
    """
    Phương án dự phòng: nhập từng cuốn sách một.
    
    Args:
        books: Danh sách sách cần nhập
        
    Returns:
        dict: Kết quả nhập dữ liệu {success_count, failed_count, failed_items}
    """
    successful = 0
    failed = 0
    failed_items = []
    
    logger.info(f"Nhập từng cuốn một: {len(books)} sách")
    
    for book in books:
        if import_book_via_api(book):
            successful += 1
        else:
            failed += 1
            failed_items.append({
                "title": book.get("title", "Unknown"),
                "error": "Failed via individual API call"
            })
            logger.error(f"Lỗi khi nhập sách '{book.get('title')}'")
    
    logger.info(f"Đã nhập thành công {successful}/{len(books)} sách vào database, {failed} sách bị lỗi")
    
    return {
        "success_count": successful,
        "failed_count": failed,
        "failed_items": failed_items
    } 