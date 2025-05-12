from typing import Optional, List
from pydantic import BaseModel, Field

class Book(BaseModel):
    """Model Pydantic cho sách."""
    id: int
    title: str
    price: Optional[str] = None
    original_price: Optional[str] = None
    discount: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        """Cấu hình model."""
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Nhà Giả Kim",
                "price": "79.000đ",
                "original_price": "100.000đ",
                "discount": "-20%",
                "author": "Paulo Coelho",
                "url": "https://www.fahasa.com/nha-gia-kim.html",
                "image_url": "https://cdn1.fahasa.com/media/catalog/product/image_195509_1_36793.jpg"
            }
        }

class BookList(BaseModel):
    """Danh sách sách với thông tin phân trang."""
    total: int
    limit: int
    offset: int
    books: List[Book]

class SearchResult(BaseModel):
    """Kết quả tìm kiếm sách."""
    keyword: str
    total: int
    limit: int
    offset: int
    books: List[Book] 