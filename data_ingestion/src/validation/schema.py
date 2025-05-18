"""
Chứa các định nghĩa schema cho việc xác thực dữ liệu.
"""

# Schema dữ liệu sách
BOOK_SCHEMA = {
    "required": ["title"],  # Các trường bắt buộc phải có
    "optional": [
        "price", "original_price", "discount", "author", "url", "image_url", "category",
        "product_code", "supplier", "publisher", "publish_year", "weight", 
        "dimensions", "page_count", "cover_type", "description", "language"
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
        "description": str,
        "language": str
    }
} 