from data_ingestion.src.config.settings import logger
from data_ingestion.src.utils.data_loader import load_json_data, get_all_data_files
from data_ingestion.src.api.book_client import delete_all_books, import_books_batch
from data_ingestion.src.validation.validator import validate_book, clean_book_data

def import_to_database(data):
    """
    Nhập dữ liệu vào database thông qua API.
    
    Args:
        data: Dữ liệu sách cần nhập
        
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    try:
        # Xác thực và làm sạch dữ liệu
        valid_books = []
        invalid_count = 0
        
        for book in data:
            if validate_book(book):
                cleaned_book = clean_book_data(book)
                valid_books.append(cleaned_book)
            else:
                invalid_count += 1
        
        if invalid_count > 0:
            logger.warning(f"Có {invalid_count}/{len(data)} sách không hợp lệ và bị bỏ qua")
        
        if not valid_books:
            logger.error("Không có sách nào hợp lệ để nhập")
            return False
        logger.info(f"Đã xác thực {len(valid_books)} sách hợp lệ")

        logger.info("Tiến hành xóa dữ liệu hiện có...")
        success, deleted_count = delete_all_books()

        if success:
            logger.info(f"Đã xóa {deleted_count} sách hiện có trong database")
        else:
            logger.warning("Không thể xóa dữ liệu hiện có, tiếp tục với dữ liệu mới")
        

        logger.info(f"Tiến hành nhập dữ liệu mới vào database...")
         
        result = import_books_batch(valid_books)
        
     
        return result["success_count"] > 0
    except Exception as e:
        logger.error(f"Lỗi khi nhập dữ liệu vào database: {e}")
        return False

def run_ingestion():
    """Hàm run_ingestion điều phối toàn bộ quá trình ingestion."""
    try:
        logger.info("Ingestion service đã khởi động...")
        # Nếu không có file tổng hợp, đọc từng file danh mục
        logger.info("Đang tìm các file dữ liệu theo danh mục...")
        all_data = []
        category_files = get_all_data_files() # các path của các file dữ liệu
        
        if not category_files:
            logger.error("Không tìm thấy file dữ liệu nào")
            return False
            
        logger.info(f"Đã tìm thấy {len(category_files)} file dữ liệu")
        
        for file_path in category_files:
            books_category_data = load_json_data(file_path) # đọc dữ liệu từ file
            if books_category_data:
                all_data.extend(books_category_data) # thêm dữ liệu vào all_data
        
        if all_data:
            success = import_to_database(all_data)
            logger.info("Quá trình nhập dữ liệu hoàn tất thành công" if success else "Quá trình nhập dữ liệu thất bại")
            return success
        else:
            logger.error("Không có dữ liệu nào để nhập")
            return False
            
    except Exception as e:
        logger.error(f"Quá trình nhập dữ liệu thất bại: {e}")
        return False