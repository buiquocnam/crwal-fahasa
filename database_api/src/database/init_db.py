from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
import time
from typing import Generator
from database_api.src.config.settings import DATABASE_URL, logger

# Tạo SQLAlchemy engine với connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, 
    pool_recycle=3600,   
    pool_size=5,         
    max_overflow=10,    
    pool_timeout=30      
)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo lớp cơ sở cho các models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Lấy phiên làm việc với cơ sở dữ liệu.
    
    Yields:
        Session: Phiên làm việc với cơ sở dữ liệu
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> bool:
    """
    Khởi tạo các bảng trong cơ sở dữ liệu với cơ chế thử lại.
    
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    max_retries = 5
    retry_interval = 3
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Đang cố gắng khởi tạo cơ sở dữ liệu (lần thử {attempt + 1}/{max_retries})")
            
            # Kiểm tra kết nối cơ sở dữ liệu
            with engine.connect() as conn:
                logger.info("Kết nối cơ sở dữ liệu thành công")
            
            # Import models ở đây để đảm bảo chúng được đăng ký với Base
            from database_api.src.models.book import BookModel
            
            # Xóa tất cả các bảng và tạo lại chúng
            Base.metadata.drop_all(bind=engine)
            logger.info("Đã xóa các bảng hiện có")
            
            # Tạo các bảng
            Base.metadata.create_all(bind=engine)
            logger.info("Các bảng cơ sở dữ liệu đã được tạo thành công")
            return True
            
        except Exception as e:
            logger.error(f"Lỗi khi khởi tạo cơ sở dữ liệu (lần thử {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                logger.warning(f"Thử lại sau {retry_interval} giây...")
                time.sleep(retry_interval)
            else:
                logger.error(f"Không thể khởi tạo cơ sở dữ liệu sau {max_retries} lần thử")
                return False
    
    return False

# Khởi tạo cơ sở dữ liệu khi module được import
try:
    if init_db():
        logger.info("Cơ sở dữ liệu đã được khởi tạo thành công")
    else:
        logger.error("Không thể khởi tạo cơ sở dữ liệu")
except Exception as e:
    logger.error(f"Lỗi không mong đợi trong quá trình khởi tạo cơ sở dữ liệu: {str(e)}")
