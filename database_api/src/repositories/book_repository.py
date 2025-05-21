from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from database_api.src.models.book import BookModel
from database_api.src.database.init_db import get_db, SessionLocal
from database_api.src.config.settings import logger

class BookRepository:
    """Repository cho các thao tác cơ sở dữ liệu sách."""
    
    def __init__(self):
        """Khởi tạo repository."""
        self.SessionLocal = SessionLocal
    
    def get_all(self, limit: int = 10, page: int = 1, title: Optional[str] = None, 
               author: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Lấy tất cả sách với phân trang và lọc.
        
        Args:
            limit: Số lượng bản ghi tối đa trả về
            page: Số trang hiện tại
            title: Lọc theo tiêu đề
            author: Lọc theo tác giả
            category: Lọc theo thể loại
            
        Returns:
            Dict[str, Any]: Dictionary chứa sách và tổng số lượng
        """
        try:
            session = self.SessionLocal()
            query = select(BookModel)
            
            # Áp dụng bộ lọc
            if title:
                query = query.filter(BookModel.title.ilike(f"%{title}%"))
            if author:
                query = query.filter(BookModel.author.ilike(f"%{author}%"))
            if category:
                query = query.filter(BookModel.category == category)
            
            # Lấy tổng số lượng
            total = session.scalar(select(func.count()).select_from(query.subquery()))
            
            # Tính offset từ page và limit
            offset = (page - 1) * limit
            
            # Áp dụng phân trang và sắp xếp
            query = query.order_by(desc(BookModel.created_at)).offset(offset).limit(limit)
            
            # Thực thi truy vấn
            books = session.scalars(query).all()
            
            # Tính total_pages
            total_pages = (total + limit - 1) // limit if total > 0 else 1
            
            result = {
                "items": books,
                "total": total,
                "limit": limit,
                "page": page,
                "total_pages": total_pages
            }
            
            # Thêm thông tin từ khóa tìm kiếm nếu có
            if title:
                result["title_keyword"] = title
            if author:
                result["author_keyword"] = author
            
            session.close()
            return result
        except Exception as e:
            logger.error(f"Lỗi khi lấy sách: {e}")
            if 'session' in locals():
                session.close()
            return {
                "items": [],
                "total": 0,
                "limit": limit,
                "page": page,
                "total_pages": 0
            }
    
    def get_by_id(self, book_id: int) -> Optional[BookModel]:
        """
        Lấy sách theo ID.
        
        Args:
            book_id: ID sách
            
        Returns:
            Optional[BookModel]: Sách nếu tìm thấy, None nếu không
        """
        try:
            session = self.SessionLocal()
            query = select(BookModel).filter(BookModel.id == book_id)
            book = session.scalar(query)
            session.close()
            return book
        except Exception as e:
            logger.error(f"Lỗi khi lấy sách {book_id}: {e}")
            if 'session' in locals():
                session.close()
            return None
    
    def create_many(self, books_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Tạo nhiều sách.
        
        Args:
            books_data: Danh sách các từ điển dữ liệu sách
            
        Returns:
            Dict[str, Any]: Kết quả với số lượng thành công và lỗi
        """
        success_count = 0
        error_count = 0
        errors = []
        
        try:
            session = self.SessionLocal()
            for book_data in books_data:
                try:
                    book = BookModel(**book_data)
                    session.add(book)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(str(e))
            
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Lỗi khi commit hàng loạt: {e}")
                session.rollback()
                return {
                    "success_count": 0,
                    "error_count": len(books_data),
                    "errors": [str(e)]
                }
            
            session.close()
            return {
                "success_count": success_count,
                "error_count": error_count,
                "errors": errors if errors else None
            }
        except Exception as e:
            logger.error(f"Lỗi trong create_many: {e}")
            if 'session' in locals():
                session.close()
            return {
                "success_count": 0,
                "error_count": len(books_data),
                "errors": [str(e)]
            }
    
    def delete_all(self) -> Dict[str, int]:
        """
        Xóa tất cả sách.
        
        Returns:
            Dict[str, int]: Số lượng sách đã xóa
        """
        try:
            session = self.SessionLocal()
            count = session.scalar(select(func.count()).select_from(BookModel))
            session.execute(delete(BookModel))
            session.commit()
            session.close()
            return {"deleted_count": count}
        except Exception as e:
            logger.error(f"Lỗi khi xóa tất cả sách: {e}")
            if 'session' in locals():
                session.close()
            return {"deleted_count": 0}
    
    def get_categories(self) -> List[str]:
        """
        Lấy danh sách tất cả các danh mục sách duy nhất.
        
        Returns:
            List[str]: Danh sách các danh mục sách
        """
        try:
            session = self.SessionLocal()
            
            # Truy vấn để lấy tất cả các danh mục duy nhất
            query = select(BookModel.category).distinct().order_by(BookModel.category)
            
            # Thực thi truy vấn và lấy kết quả
            categories = [cat[0] for cat in session.execute(query).all() if cat[0]]
            
            session.close()
            return categories
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách danh mục: {e}")
            if 'session' in locals():
                session.close()
            return [] 