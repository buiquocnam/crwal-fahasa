"""
Chứa các ánh xạ (mapping) cho quá trình xác thực và chuyển đổi dữ liệu.
"""

# Mapping cho các trường dữ liệu từ Fahasa sang hệ thống
KEY_MAPPING = {
    # Tiếng Anh
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
    "language": "language",
    "translator": "translator",
    
    # Tiếng Việt
    "mã hàng": "product_code",
    "tên nhà cung cấp": "supplier",
    "nhà cung cấp": "supplier", 
    "tác giả": "author",
    "nxb": "publisher",
    "năm xb": "publish_year",
    "công ty phát hành": "distributor",
    "kích thước bao bì": "dimensions",
    "hình thức": "cover_type",
    "số trang": "page_count",
    "trọng lượng (gr)": "weight",
    "người dịch": "translator", 
    "ngôn ngữ": "language",
    
    # Dữ liệu đã chuẩn hóa (underscore)
    "người_dịch": "translator",
    "ngôn_ngữ": "language",
    "nhà_xuất_bản": "publisher",
    "dự_kiến_có_hàng": "publish_year"
} 