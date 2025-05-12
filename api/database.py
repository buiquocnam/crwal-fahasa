import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Generator
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, logger

def get_db_connection():
    """Lấy kết nối đến cơ sở dữ liệu PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )

def wait_for_postgres():
    """Đợi cho PostgreSQL sẵn sàng."""
    max_retries = 30
    retry_count = 0
    
    logger.info("Đang đợi PostgreSQL sẵn sàng...")
    
    while retry_count < max_retries:
        try:
            conn = get_db_connection()
            conn.close()
            logger.info("PostgreSQL đã sẵn sàng!")
            return True
        except psycopg2.OperationalError:
            retry_count += 1
            logger.info(f"PostgreSQL chưa sẵn sàng. Thử lại {retry_count}/{max_retries}")
            time.sleep(2)
    
    logger.error("Không thể kết nối đến PostgreSQL")
    return False

def get_db() -> Generator:
    """Dependency để lấy kết nối database và quản lý vòng đời kết nối."""
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    finally:
        if conn is not None:
            conn.close()
            logger.debug("Đã đóng kết nối database") 