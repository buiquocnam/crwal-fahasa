from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from ..repositories.book_repository import BookRepository
from ..models.book import BookCreate, Book, BookList, BatchBookResult
from database_api.src.config.settings import logger
 
class BookService:
    """Dịch vụ xử lý logic nghiệp vụ cho sách."""
    
    def __init__(self):
        """Khởi tạo dịch vụ."""
        self.repository = BookRepository()
    
    def get_books(self, limit: int = 10, page: int = 1, keyword: Optional[str] = None, 
                 search_type: str = "title", category: Optional[str] = None) -> BookList:
        """
        Lấy tất cả sách hoặc tìm kiếm sách với phân trang và lọc.
        
        Tham số:
            limit: Số lượng bản ghi tối đa trả về
            page: Số trang hiện tại
            keyword: Từ khóa tìm kiếm (nếu có)
            search_type: Loại tìm kiếm (title, author, category)
            category: Lọc theo thể loại
            
        Trả về:
            BookList: Danh sách sách đã phân trang
            
        Ngoại lệ:
            HTTPException: Nếu có lỗi khi truy xuất sách
        """
        try:
            # Khởi tạo các tham số cho phương thức get_all
            params = {
                "limit": limit,
                "page": page,
                "category": category
            }
            
            # Thêm tham số tìm kiếm dựa trên search_type
            if keyword:
                if search_type == "title":
                    params["title"] = keyword
                elif search_type == "author":
                    params["author"] = keyword
                elif search_type == "category":
                    params["category"] = keyword
                else:
                    raise HTTPException(status_code=400, detail="Loại tìm kiếm không hợp lệ")
            
            # Gọi phương thức get_all với các tham số
            result = self.repository.get_all(**params)
            
            # Chuyển đổi kết quả từ repository thành BookList
            return BookList(
                items=[Book.from_orm(book) for book in result["items"]],
                total=result["total"],
                limit=result["limit"],
                page=result["page"],
                total_pages=result["total_pages"]
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Lỗi khi lấy hoặc tìm kiếm sách: {e}")
            raise HTTPException(status_code=500, detail="Lỗi khi truy xuất sách")
    
    def get_categories(self) -> List[str]:
        """
        Lấy danh sách tất cả các danh mục sách.
        
        Trả về:
            List[str]: Danh sách các danh mục sách
            
        Ngoại lệ:
            HTTPException: Nếu có lỗi khi truy xuất danh mục
        """
        try:
            # Gọi phương thức từ repository để lấy danh sách danh mục
            categories = self.repository.get_categories()
            return categories
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách danh mục: {e}")
            raise HTTPException(status_code=500, detail="Lỗi khi truy xuất danh mục sách")
    
    def get_book(self, book_id: int) -> Book:
        """
        Lấy sách theo ID.
        
        Tham số:
            book_id: ID của sách
            
        Trả về:
            Book: Dữ liệu sách
            
        Ngoại lệ:
            HTTPException: Nếu không tìm thấy sách hoặc có lỗi xảy ra
        """
        try:
            book = self.repository.get_by_id(book_id)
            if not book:
                raise HTTPException(status_code=404, detail="Không tìm thấy sách")
            return Book.from_orm(book)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Lỗi khi lấy thông tin sách: {e}")
            raise HTTPException(status_code=500, detail="Lỗi khi truy xuất sách")

    def create_books(self, books_data: List[BookCreate]) -> BatchBookResult:
        """
        Tạo nhiều sách.
        
        Tham số:
            books_data: Danh sách dữ liệu sách
            
        Trả về:
            BatchBookResult: Kết quả với số lượng thành công và lỗi
            
        Ngoại lệ:
            HTTPException: Nếu tất cả việc tạo đều thất bại
        """
        try:
            result = self.repository.create_many([book.dict() for book in books_data])
            if result["success_count"] == 0:
                raise HTTPException(status_code=400, detail="Lỗi khi tạo sách")
            return BatchBookResult(**result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Lỗi khi tạo sách: {e}")
            raise HTTPException(status_code=500, detail="Lỗi khi tạo sách")   
    
    def delete_all_books(self) -> Dict[str, int]:
        """
        Xóa tất cả sách.
        
        Trả về:
            Dict[str, int]: Số lượng sách đã xóa
            
        Ngoại lệ:
            HTTPException: Nếu việc xóa thất bại
        """
        try:
            result = self.repository.delete_all()
            return result
        except Exception as e:
            logger.error(f"Lỗi khi xóa tất cả sách: {e}")
            raise HTTPException(status_code=500, detail="Lỗi khi xóa tất cả sách") 