import json
import os
import time
import psycopg2
import logging
from psycopg2 import sql

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Các hằng số
DATA_FILE = "/app/data/fahasa_data.json"
DB_HOST = "postgres"
DB_NAME = "fahasa_db"
DB_USER = "fahasa"
DB_PASSWORD = "fahasa123"
DB_PORT = 5432

# Câu lệnh SQL
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price TEXT,
    discount_price TEXT,
    author TEXT,
    url TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_BOOK_SQL = """
INSERT INTO books (title, price, discount_price, author, url, image_url)
VALUES (%s, %s, %s, %s, %s, %s)
"""

def wait_for_postgres():
    """Đợi cho PostgreSQL sẵn sàng."""
    max_retries = 30
    retry_count = 0
    
    logger.info("Đang đợi PostgreSQL sẵn sàng...")
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            conn.close()
            logger.info("PostgreSQL đã sẵn sàng!")
            return True
        except psycopg2.OperationalError:
            retry_count += 1
            logger.info(f"PostgreSQL chưa sẵn sàng. Thử lại {retry_count}/{max_retries}")
            time.sleep(2)
    
    logger.error("Không thể kết nối đến PostgreSQL")
    return False

def setup_database():
    """Thiết lập cấu trúc cơ sở dữ liệu."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
            logger.info("Thiết lập cấu trúc cơ sở dữ liệu thành công")
        
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Lỗi khi thiết lập cơ sở dữ liệu: {e}")
        return False

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

def import_to_postgres(data):
    """Nhập dữ liệu vào PostgreSQL."""
    if not data:
        logger.error("Không có dữ liệu để nhập")
        return False
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        with conn.cursor() as cursor:
            # Kiểm tra xem đã có dữ liệu chưa
            cursor.execute("SELECT COUNT(*) FROM books")
            count = cursor.fetchone()[0]
            
            if count > 0:
                logger.info(f"Cơ sở dữ liệu đã chứa {count} sách. Bỏ qua việc nhập.")
                conn.close()
                return True
            
            # Nhập dữ liệu
            for book in data:
                cursor.execute(
                    INSERT_BOOK_SQL,
                    (
                        book.get('title'),
                        book.get('price'),
                        book.get('discount_price'),
                        book.get('author'),
                        book.get('url'),
                        book.get('image_url')
                    )
                )
            
            conn.commit()
            logger.info(f"Đã nhập thành công {len(data)} sách vào PostgreSQL")
        
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Lỗi khi nhập dữ liệu vào PostgreSQL: {e}")
        return False

def main():
    try:
        # Đợi PostgreSQL sẵn sàng
        if not wait_for_postgres():
            return
        
        # Đợi file dữ liệu sẵn sàng (crawler có thể vẫn đang chạy)
        max_retries = 30
        retry_count = 0
        
        while retry_count < max_retries and not os.path.exists(DATA_FILE):
            logger.info(f"Đang đợi file dữ liệu... {retry_count + 1}/{max_retries}")
            time.sleep(5)
            retry_count += 1
        
        if not os.path.exists(DATA_FILE):
            logger.error(f"Không tìm thấy file dữ liệu sau {max_retries} lần thử: {DATA_FILE}")
            return
        
        # Thiết lập cấu trúc cơ sở dữ liệu
        if not setup_database():
            return
        
        # Đọc dữ liệu từ JSON
        data = load_json_data(DATA_FILE)
        
        # Nhập vào PostgreSQL
        import_to_postgres(data)
        
        logger.info("Quá trình nhập dữ liệu hoàn tất thành công")
    except Exception as e:
        logger.error(f"Quá trình nhập dữ liệu thất bại: {e}")

if __name__ == "__main__":
    main() 