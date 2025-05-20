import requests
from typing import Dict, Optional, List, Any
from config.settings import logger

class Book:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_books(
        self, 
        limit: int = 10, 
        page: int = 1, 
        keyword: Optional[str] = None, 
        search_type: str = 'title', 
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lấy danh sách tất cả sách hoặc tìm kiếm sách
        
        Tham số:
            limit: Số lượng sách tối đa trả về
            page: Trang hiện tại
            keyword: Từ khóa tìm kiếm (nếu có)
            search_type: Loại tìm kiếm (title, author, category)
            category: Danh mục sách (nếu có)
            
        Trả về:
            Dict: Kết quả danh sách hoặc tìm kiếm sách
        """
        try:
            params = {
                "limit": limit,
                "page": page
            }
            
            # Thêm tham số tìm kiếm nếu có
            if keyword:
                params["keyword"] = keyword
                params["search_type"] = search_type
                
            # Thêm tham số danh mục nếu có
            if category:
                params["category"] = category
                
            response = requests.get(
                f"{self.api_url}/books",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            logger.error(f"Lỗi khi lấy sách: Status code {response.status_code}, Response: {response.text}")
            return {"items": [], "total": 0, "page": page, "total_pages": 0}
        except requests.RequestException as e:
            logger.error(f"Lỗi khi lấy hoặc tìm kiếm sách: {e}")
            return {"items": [], "total": 0, "page": page, "total_pages": 0}

    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin chi tiết sách theo ID
        
        Tham số:
            book_id: ID của sách cần lấy thông tin
            
        Trả về:
            Optional[Dict]: Thông tin chi tiết sách nếu tìm thấy, None nếu không tìm thấy
        """
        try:
            response = requests.get(f"{self.api_url}/books/{book_id}")
            if response.status_code == 200:
                return response.json()
            if response.status_code == 404:
                logger.warning(f"Không tìm thấy sách với ID {book_id}")
            else:
                logger.error(f"Lỗi khi lấy sách {book_id}: Status code {response.status_code}, Response: {response.text}")
            return None
        except requests.RequestException as e:
            logger.error(f"Lỗi khi lấy thông tin chi tiết sách: {e}")
            return None

    def get_categories(self) -> List[str]:
        """
        Lấy danh sách tất cả các danh mục sách
        
        Trả về:
            List[str]: Danh sách các danh mục sách
        """
        try:
            response = requests.get(f"{self.api_url}/books/categories/list")
            if response.status_code == 200:
                return response.json()
            logger.error(f"Lỗi khi lấy danh mục: Status code {response.status_code}, Response: {response.text}")
            return []
        except requests.RequestException as e:
            logger.error(f"Lỗi khi lấy danh sách danh mục: {e}")
            return [] 