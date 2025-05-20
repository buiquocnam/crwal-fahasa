from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from database_api.src.database.init_db import Base

class BookModel(Base):
    """Mô hình SQLAlchemy cho bảng sách."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    price = Column(String(50), nullable=True)
    original_price = Column(String(50), nullable=True)
    discount = Column(String(50), nullable=True)
    image_url = Column(String(500), nullable=True)
    product_code = Column(String(100), nullable=True)
    supplier = Column(String(255), nullable=True)
    author = Column(String(255), nullable=True)
    publisher = Column(String(255), nullable=True)
    publish_year = Column(String(50), nullable=True)
    weight = Column(String(50), nullable=True)
    dimensions = Column(String(100), nullable=True)
    page_count = Column(String(50), nullable=True)
    cover_type = Column(String(100), nullable=True)
    url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    language = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"

# Các mô hình Pydantic cho yêu cầu/phản hồi
class BookBase(BaseModel):
    """Mô hình cơ sở cho dữ liệu sách."""
    title: str = Field(..., min_length=1, max_length=255)
    price: Optional[str] = None
    original_price: Optional[str] = None
    discount: Optional[str] = None
    image_url: Optional[str] = None
    product_code: Optional[str] = None
    supplier: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[str] = None
    weight: Optional[str] = None
    dimensions: Optional[str] = None
    page_count: Optional[str] = None
    cover_type: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None

class BookCreate(BookBase):
    """Mô hình để tạo sách."""
    pass

class BookUpdate(BaseModel):
    """Mô hình để cập nhật sách."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[str] = None
    original_price: Optional[str] = None
    discount: Optional[str] = None
    image_url: Optional[str] = None
    product_code: Optional[str] = None
    supplier: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[str] = None
    weight: Optional[str] = None
    dimensions: Optional[str] = None
    page_count: Optional[str] = None
    cover_type: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None

class Book(BookBase):
    """Mô hình cho phản hồi sách."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookList(BaseModel):
    """Mô hình cho danh sách sách và kết quả tìm kiếm."""
    items: List[Book]
    total: int
    limit: int
    page: int = 1
    total_pages: int = 1
    keyword: Optional[str] = None

class BatchBookResult(BaseModel):
    """Mô hình cho kết quả thao tác hàng loạt."""
    success_count: int
    error_count: int
    errors: Optional[List[str]] = None 