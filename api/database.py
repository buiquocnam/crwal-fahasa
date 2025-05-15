from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from contextlib import contextmanager

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Lấy thông tin kết nối từ biến môi trường
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "books_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Tạo Base cho các model
Base = declarative_base()

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency để cung cấp session database cho các API endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model SQLAlchemy cho bảng books
class BookDB(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(String)
    original_price = Column(String)
    discount = Column(String)
    image_url = Column(String)
    product_code = Column(String)
    supplier = Column(String)
    author = Column(String)
    publisher = Column(String)
    publish_year = Column(String)
    weight = Column(String)
    dimensions = Column(String)
    page_count = Column(String)
    cover_type = Column(String)
    url = Column(String)
    description = Column(String)
    category = Column(String)

def create_tables():
    """Tạo bảng nếu chưa tồn tại."""
    try:
        logger.info("Tạo bảng books...")
        Base.metadata.create_all(bind=engine)
        logger.info("Đã tạo hoặc xác nhận bảng books thành công!")
        return True
    except Exception as e:
        logger.error(f"Lỗi khi tạo bảng: {e}")
        return False

def init_db():
    """Khởi tạo kết nối và cấu trúc database."""
    try:
        # Tạo bảng nếu chưa tồn tại
        create_tables()
        logger.info("Khởi tạo database thành công!")
        return True
    except Exception as e:
        logger.error(f"Lỗi khởi tạo database: {e}")
        return False 