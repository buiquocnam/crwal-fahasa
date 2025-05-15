from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Book(BaseModel):
    """Model Pydantic cho sách."""
    id: Optional[int]
    title: str
    price: Optional[str]
    original_price: Optional[str]
    discount: Optional[str]
    image_url: Optional[str]
    product_code: Optional[str]
    supplier: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    publish_year: Optional[str]
    weight: Optional[str]
    dimensions: Optional[str]
    page_count: Optional[str]
    cover_type: Optional[str]
    url: Optional[str]
    description: Optional[str]
    category: Optional[str]
    
    class Config:
        orm_mode = True
        
class BookCreate(BaseModel):
    """Model cho việc tạo sách mới không cần ID."""
    title: str
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
    
    class Config:
        orm_mode = True

class BatchBookResult(BaseModel):
    """Kết quả nhập nhiều sách cùng lúc."""
    total: int
    success_count: int
    failed_count: int
    failed_items: List[Dict[str, Any]] = []

class BookList(BaseModel):
    """Danh sách sách với thông tin phân trang."""
    total: int
    limit: int
    offset: int
    books: List[Book]
    
    class Config:
        orm_mode = True

class SearchResult(BaseModel):
    """Kết quả tìm kiếm sách."""
    keyword: str
    total: int
    limit: int
    offset: int
    books: List[Book]
    
    class Config:
        orm_mode = True 