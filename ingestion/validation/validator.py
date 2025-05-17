from ingestion.config.settings import VIETNAMESE_PATTERN, logger
from ingestion.validation.schema import BOOK_SCHEMA
from ingestion.validation.mappings import KEY_MAPPING

def validate_book(book, index=None):
    """
    Kiểm tra tính hợp lệ của dữ liệu sách.
    
    Args:
        book: Thông tin sách cần kiểm tra
        index: Chỉ số hoặc ID để hiển thị trong log
        
    Returns:
        bool: True nếu dữ liệu hợp lệ, False nếu không
    """
    book_id = index if index is not None else book.get('id', 'Unknown')
    
    # Kiểm tra các trường bắt buộc
    for field in BOOK_SCHEMA["required"]:
        if field not in book or book[field] is None or book[field] == "":
            logger.error(f"Sách {book_id}: Thiếu trường bắt buộc '{field}'")
            return False
    
    # Kiểm tra kiểu dữ liệu
    for field, field_type in BOOK_SCHEMA["types"].items():
        if field in book and book[field] is not None:
            if not isinstance(book[field], field_type):
                logger.error(f"Sách {book_id}: Trường '{field}' có kiểu dữ liệu không hợp lệ, mong đợi {field_type.__name__}")
                return False
    
    # Các kiểm tra tùy chỉnh
    if "url" in book and book["url"]:
        if not book["url"].startswith("http"):
            logger.warning(f"Sách {book_id}: URL không bắt đầu bằng http: {book['url']}")
    
    # Dữ liệu tiếng Việt
    if "title" in book and book["title"]:
        # Kiểm tra xem có ký tự tiếng Việt không (có dấu)
        if VIETNAMESE_PATTERN.search(book["title"]) and not isinstance(book["title"], str):
            logger.warning(f"Sách {book_id}: Tiêu đề có thể chứa ký tự tiếng Việt nhưng không phải chuỗi Unicode")
    
    return True

def clean_book_data(book):
    """
    Làm sạch và chuẩn hóa dữ liệu sách.
    
    Args:
        book: Dữ liệu sách cần làm sạch
        
    Returns:
        dict: Dữ liệu sách đã được làm sạch
    """
    cleaned_book = {}
    
    # Giữ lại các trường có trong schema dữ liệu
    valid_fields = BOOK_SCHEMA["required"] + BOOK_SCHEMA["optional"]
    for field in valid_fields:
        if field in book:
            cleaned_book[field] = book[field]
    
    return cleaned_book 