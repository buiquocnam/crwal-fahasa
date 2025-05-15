import json
import os
import time
import requests
import logging
import glob
import re

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Các hằng số
DATA_DIR = "/app/data"
COMBINED_DATA_FILE = "/app/data/fahasa_data.json"  # File tổng hợp
API_BASE_URL = "http://api:8000"  # URL của API service trong Docker

# Schema dữ liệu cần thiết
BOOK_SCHEMA = {
    "required": ["title"],  # Các trường bắt buộc phải có
    "optional": [
        "price", "original_price", "discount", "author", "url", "image_url", "category",
        "product_code", "supplier", "publisher", "publish_year", "weight", 
        "dimensions", "page_count", "cover_type", "description"
    ],
    "types": {
        "title": str,
        "price": str,
        "original_price": str,
        "discount": str,
        "author": str,
        "url": str,
        "image_url": str,
        "category": str,
        "product_code": str,
        "supplier": str,
        "publisher": str,
        "publish_year": str,
        "weight": str,
        "dimensions": str,
        "page_count": str,
        "cover_type": str,
        "description": str
    }
}

def validate_book(book, index=None):
    """Kiểm tra tính hợp lệ của dữ liệu sách."""
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
        vietnamese_pattern = re.compile(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', re.IGNORECASE)
        if vietnamese_pattern.search(book["title"]) and not isinstance(book["title"], str):
            logger.warning(f"Sách {book_id}: Tiêu đề có thể chứa ký tự tiếng Việt nhưng không phải chuỗi Unicode")
    
    return True

def clean_book_data(book):
    """Làm sạch và chuẩn hóa dữ liệu sách."""
    cleaned_book = {}
    
    # Xử lý các trường đặc biệt theo tên gốc từ Fahasa và ánh xạ vào BookDB
    field_mapping = {
        "title": "title",
        "price": "price",
        "original_price": "original_price",
        "discount": "discount", 
        "author": "author",
        "url": "url",
        "image_url": "image_url",
        "category": "category",
        "product_code": "product_code",
        "supplier": "supplier",
        "publisher": "publisher",
        "publish_year": "publish_year",
        "weight": "weight",
        "dimensions": "dimensions",
        "page_count": "page_count",
        "cover_type": "cover_type",
        "description": "description",
        # Các trường bổ sung tiếng Việt cần được ánh xạ
        "người_dịch": "author",  # Ghép người dịch vào author
        "ngôn_ngữ": "category",  # Thêm thông tin ngôn ngữ vào category
        "nhà_xuất_bản": "publisher",
        "dự_kiến_có_hàng": "publish_year"
    }
    
    # Duyệt qua tất cả các trường trong dữ liệu gốc
    for field, value in book.items():
        # Chuẩn hóa tên trường (lowercase và gạch dưới thay cho khoảng trắng)
        normalized_field = field.lower().replace(" ", "_")
        
        # Kiểm tra xem trường có ánh xạ không
        if normalized_field in field_mapping:
            target_field = field_mapping[normalized_field]
            
            # Trường hợp đặc biệt: ghép người dịch vào author
            if normalized_field == "người_dịch" and "author" in cleaned_book:
                cleaned_book["author"] = f"{cleaned_book['author']} (Dịch: {value})"
            # Trường hợp đặc biệt: thêm ngôn ngữ vào category
            elif normalized_field == "ngôn_ngữ" and "category" in cleaned_book:
                cleaned_book["category"] = f"{cleaned_book['category']} - {value}"
            else:
                cleaned_book[target_field] = value
    
    # Giữ lại các trường có trong schema dữ liệu
    valid_fields = BOOK_SCHEMA["required"] + BOOK_SCHEMA["optional"]
    for field in valid_fields:
        if field in book:
            cleaned_book[field] = book[field]
    
    # Xử lý tiêu đề
    if "title" in cleaned_book:
        cleaned_book["title"] = cleaned_book["title"].strip()
    
    # Xử lý URL
    if "url" in cleaned_book and cleaned_book["url"]:
        if not cleaned_book["url"].startswith("http"):
            cleaned_book["url"] = "https://" + cleaned_book["url"].lstrip(":/")
    
    # Đảm bảo category có giá trị
    if "category" not in cleaned_book or not cleaned_book["category"]:
        cleaned_book["category"] = "uncategorized"
    
    return cleaned_book

def load_json_data(file_path):
    """Đọc dữ liệu từ file JSON."""
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

def wait_for_data_files():
    """Đợi cho các file dữ liệu sẵn sàng."""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        # Kiểm tra file tổng hợp
        if os.path.exists(COMBINED_DATA_FILE):
            logger.info(f"Đã tìm thấy file dữ liệu tổng hợp: {COMBINED_DATA_FILE}")
            return True
        
        # Kiểm tra các file theo danh mục
        category_files = glob.glob(os.path.join(DATA_DIR, "fahasa_*.json"))
        if category_files:
            logger.info(f"Đã tìm thấy {len(category_files)} file dữ liệu theo danh mục")
            return True
        
        logger.info(f"Đang đợi file dữ liệu... {retry_count + 1}/{max_retries}")
        time.sleep(5)
        retry_count += 1
    
    logger.error(f"Không tìm thấy file dữ liệu sau {max_retries} lần thử")
    return False

def import_book_via_api(book):
    """Nhập một cuốn sách thông qua API."""
    try:
        # In ra thông tin sách để debug
        logger.info(f"Thêm sách: {book.get('title')}, Dữ liệu: {json.dumps(book, ensure_ascii=False)}")
        
        # Sử dụng endpoint POST /books thay vì /books/add
        response = requests.post(f"{API_BASE_URL}/books", json=book)
        if response.status_code in [200, 201]:
            return True
        else:
            logger.error(f"Lỗi khi thêm sách qua API: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Lỗi khi gửi request thêm sách: {e}")
        return False

def import_to_database(data):
    """Nhập dữ liệu vào database thông qua API."""
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
        
        # Sử dụng endpoint batch để nhập nhiều sách cùng lúc
        logger.info(f"Đang nhập {len(valid_books)} sách qua API endpoint batch...")
        try:
            response = requests.post(f"{API_BASE_URL}/books/batch", json=valid_books)
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"Đã nhập thành công {result.get('success_count')} sách vào database")
                
                if result.get('failed_count', 0) > 0:
                    logger.warning(f"Có {result.get('failed_count')} sách không thể nhập")
                    for failed in result.get('failed_items', []):
                        logger.warning(f"- Sách '{failed.get('title')}': {failed.get('error')}")
                
                return result.get('success_count', 0) > 0
            else:
                logger.error(f"Lỗi khi nhập sách qua API batch: {response.status_code} - {response.text}")
                
                # Phương án dự phòng: nhập từng cuốn một
                logger.info("Sử dụng phương án dự phòng: nhập từng cuốn một")
                successful = 0
                failed = 0
                
                for book in valid_books:
                    if import_book_via_api(book):
                        successful += 1
                    else:
                        failed += 1
                        logger.error(f"Lỗi khi nhập sách '{book.get('title')}'")
                
                logger.info(f"Đã nhập thành công {successful}/{len(valid_books)} sách vào database, {failed} sách bị lỗi")
                return successful > 0
        except Exception as e:
            logger.error(f"Lỗi khi sử dụng endpoint batch: {e}")
            logger.info("Chuyển sang phương án dự phòng: nhập từng cuốn một")
            
            # Phương án dự phòng: nhập từng cuốn một
            successful = 0
            failed = 0
            
            for book in valid_books:
                if import_book_via_api(book):
                    successful += 1
                else:
                    failed += 1
                    logger.error(f"Lỗi khi nhập sách '{book.get('title')}'")
            
            logger.info(f"Đã nhập thành công {successful}/{len(valid_books)} sách vào database, {failed} sách bị lỗi")
            return successful > 0
    except Exception as e:
        logger.error(f"Lỗi khi nhập dữ liệu vào database: {e}")
        return False

def main():
    try:
        logger.info("Ingestion service đã khởi động...")
        
        # Đợi file dữ liệu sẵn sàng (crawler có thể vẫn đang chạy)
        if not wait_for_data_files():
            return
        
        # Ưu tiên sử dụng file tổng hợp nếu có
        if os.path.exists(COMBINED_DATA_FILE):
            data = load_json_data(COMBINED_DATA_FILE)
            if data:
                import_to_database(data)
        else:
            # Nếu không có file tổng hợp, đọc từng file danh mục
            all_data = []
            category_files = glob.glob(os.path.join(DATA_DIR, "fahasa_*.json"))
            
            for file_path in category_files:
                category_data = load_json_data(file_path)
                if category_data:
                    all_data.extend(category_data)
            
            if all_data:
                import_to_database(all_data)
        
        logger.info("Quá trình nhập dữ liệu hoàn tất thành công")
    except Exception as e:
        logger.error(f"Quá trình nhập dữ liệu thất bại: {e}")

if __name__ == "__main__":
    main() 