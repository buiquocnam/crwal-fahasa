from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from database_api.src.database.init_db import Base

class BookModel(Base):
    """SQLAlchemy model for books table."""
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

# Pydantic models for request/response
class BookBase(BaseModel):
    """Base model for book data."""
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
    """Model for creating a book."""
    pass

class BookUpdate(BaseModel):
    """Model for updating a book."""
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
    """Model for book response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookList(BaseModel):
    """Model for paginated list of books."""
    items: List[Book]
    total: int
    limit: int
    offset: int

class SearchResult(BaseModel):
    """Model for search results."""
    items: List[Book]
    total: int
    limit: int
    offset: int
    keyword: Optional[str] = None

class BatchBookResult(BaseModel):
    """Model for batch operation results."""
    success_count: int
    error_count: int
    errors: Optional[List[str]] = None 