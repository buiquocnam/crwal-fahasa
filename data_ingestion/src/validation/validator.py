from data_ingestion.src.config.settings import  logger
from data_ingestion.src.validation.schema import BOOK_SCHEMA

def validate_book(book):
    """
    Kiểm tra tính hợp lệ của dữ liệu sách.
    
    Args:
        book: Thông tin sách cần kiểm tra
        
    Returns:
        bool: True nếu dữ liệu hợp lệ, False nếu không
    """
    
    # Kiểm tra các trường bắt buộc
    for field in BOOK_SCHEMA["required"]:
        if field not in book or book[field] is None or book[field] == "":
            return False
    
    # Kiểm tra kiểu dữ liệu
    for field, field_type in BOOK_SCHEMA["types"].items():
        if field in book and book[field] is not None:
            if not isinstance(book[field], field_type):
                logger.error(f"Sách {book}: Trường '{field}' có kiểu dữ liệu không hợp lệ, mong đợi {field_type.__name__}")
                return False
 
    
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