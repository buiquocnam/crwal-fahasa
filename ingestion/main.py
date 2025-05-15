import time
from ingestion.config.settings import COMBINED_DATA_FILE, logger
from ingestion.utils.data_loader import load_json_data, get_all_data_files
from ingestion.utils.api_client import import_books_batch, import_books_one_by_one
from ingestion.validation.validator import validate_book, clean_book_data

def import_to_database(data):
    """
    Nhập dữ liệu vào database thông qua API.
    
    Args:
        data: Dữ liệu sách cần nhập
        
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    if not data:
        logger.error("Không có dữ liệu để nhập")
        return False
    
    try:
        # Xác thực và làm sạch dữ liệu
        valid_books = []
        invalid_count = 0
        
        for i, book in enumerate(data):
            if validate_book(book, i):
                cleaned_book = clean_book_data(book)
                valid_books.append(cleaned_book)
            else:
                invalid_count += 1
        
        if invalid_count > 0:
            logger.warning(f"Có {invalid_count}/{len(data)} sách không hợp lệ và bị bỏ qua")
        
        if not valid_books:
            logger.error("Không có sách nào hợp lệ để nhập")
            return False
        
        logger.info(f"Đã xác thực {len(valid_books)} sách hợp lệ. Tiến hành nhập vào database...")
        
        # Thử sử dụng API endpoint batch trước
        result = import_books_batch(valid_books)
        
        # Nếu thất bại hoàn toàn, dùng phương án dự phòng
        if result["success_count"] == 0 and result["failed_count"] > 0:
            logger.info("Chuyển sang phương án dự phòng: nhập từng cuốn một")
            result = import_books_one_by_one(valid_books)
        
        return result["success_count"] > 0
    except Exception as e:
        logger.error(f"Lỗi khi nhập dữ liệu vào database: {e}")
        return False

def main():
    """Hàm main điều phối toàn bộ quá trình ingestion."""
    try:
        logger.info("Ingestion service đã khởi động...")
        
        # Ưu tiên sử dụng file tổng hợp nếu có
        if COMBINED_DATA_FILE:
            logger.info(f"Đang kiểm tra file dữ liệu tổng hợp: {COMBINED_DATA_FILE}")
            data = load_json_data(COMBINED_DATA_FILE)
            if data:
                logger.info(f"Đã tìm thấy và đọc dữ liệu từ file tổng hợp: {COMBINED_DATA_FILE}")
                import_to_database(data)
                logger.info("Quá trình nhập dữ liệu hoàn tất thành công")
                return True
            else:
                logger.warning(f"Không thể đọc dữ liệu từ file tổng hợp: {COMBINED_DATA_FILE}")
        
        # Nếu không có file tổng hợp, đọc từng file danh mục
        logger.info("Đang tìm các file dữ liệu theo danh mục...")
        all_data = []
        category_files = get_all_data_files()
        
        if not category_files:
            logger.error("Không tìm thấy file dữ liệu nào")
            return False
            
        logger.info(f"Đã tìm thấy {len(category_files)} file dữ liệu")
        
        for file_path in category_files:
            category_data = load_json_data(file_path)
            if category_data:
                all_data.extend(category_data)
        
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

if __name__ == "__main__":
    main() 