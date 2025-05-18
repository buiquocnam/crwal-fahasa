from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from database_api.src.models.book import BookModel
from database_api.src.database.init_db import get_db, SessionLocal
from database_api.src.config.settings import logger

class BookRepository:
    """Repository for book database operations."""
    
    def __init__(self):
        """Initialize repository."""
        self.SessionLocal = SessionLocal
    
    def get_all(self, limit: int = 100, offset: int = 0, title: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all books with pagination and filtering.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            title: Filter by title
            category: Filter by category
            
        Returns:
            Dict[str, Any]: Dictionary containing books and total count
        """
        try:
            session = self.SessionLocal()
            query = select(BookModel)
            
            # Apply filters
            if title:
                query = query.filter(BookModel.title.ilike(f"%{title}%"))
            if category:
                query = query.filter(BookModel.category == category)
            
            # Get total count
            total = session.scalar(select(func.count()).select_from(query.subquery()))
            
            # Apply pagination and ordering
            query = query.order_by(desc(BookModel.created_at)).offset(offset).limit(limit)
            
            # Execute query
            books = session.scalars(query).all()
            
            result = {
                "items": books,
                "total": total,
                "limit": limit,
                "offset": offset
            }
            
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error getting books: {e}")
            if 'session' in locals():
                session.close()
            return {
                "items": [],
                "total": 0,
                "limit": limit,
                "offset": offset
            }
    
    def get_by_id(self, book_id: int) -> Optional[BookModel]:
        """
        Get book by ID.
        
        Args:
            book_id: Book ID
            
        Returns:
            Optional[BookModel]: Book if found, None otherwise
        """
        try:
            session = self.SessionLocal()
            query = select(BookModel).filter(BookModel.id == book_id)
            book = session.scalar(query)
            session.close()
            return book
        except Exception as e:
            logger.error(f"Error getting book {book_id}: {e}")
            if 'session' in locals():
                session.close()
            return None
    
    def create_many(self, books_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple books.
        
        Args:
            books_data: List of book data dictionaries
            
        Returns:
            Dict[str, Any]: Results with success and error counts
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
                logger.error(f"Error committing batch: {e}")
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
            logger.error(f"Error in create_many: {e}")
            if 'session' in locals():
                session.close()
            return {
                "success_count": 0,
                "error_count": len(books_data),
                "errors": [str(e)]
            }
    
    def delete_all(self) -> Dict[str, int]:
        """
        Delete all books.
        
        Returns:
            Dict[str, int]: Number of deleted books
        """
        try:
            session = self.SessionLocal()
            count = session.scalar(select(func.count()).select_from(BookModel))
            session.execute(delete(BookModel))
            session.commit()
            session.close()
            return {"deleted_count": count}
        except Exception as e:
            logger.error(f"Error deleting all books: {e}")
            if 'session' in locals():
                session.close()
            return {"deleted_count": 0}
    
    def search_by_title(self, keyword: str, limit: int = 100, offset: int = 0, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Search books by title.
        
        Args:
            keyword: Search keyword
            limit: Maximum number of records to return
            offset: Number of records to skip
            category: Filter by category
            
        Returns:
            Dict[str, Any]: Search results
        """
        try:
            session = self.SessionLocal()
            query = select(BookModel).filter(BookModel.title.ilike(f"%{keyword}%"))
            
            if category:
                query = query.filter(BookModel.category == category)
            
            total = session.scalar(select(func.count()).select_from(query.subquery()))
            books = session.scalars(query.order_by(desc(BookModel.created_at)).offset(offset).limit(limit)).all()
            
            result = {
                "items": books,
                "total": total,
                "limit": limit,
                "offset": offset,
                "keyword": keyword
            }
            
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error searching books by title: {e}")
            if 'session' in locals():
                session.close()
            return {
                "items": [],
                "total": 0,
                "limit": limit,
                "offset": offset,
                "keyword": keyword
            }
    
    def search_by_author(self, keyword: str, limit: int = 100, offset: int = 0, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Search books by author.
        
        Args:
            keyword: Search keyword
            limit: Maximum number of records to return
            offset: Number of records to skip
            category: Filter by category
            
        Returns:
            Dict[str, Any]: Search results
        """
        try:
            session = self.SessionLocal()
            query = select(BookModel).filter(BookModel.author.ilike(f"%{keyword}%"))
            
            if category:
                query = query.filter(BookModel.category == category)
            
            total = session.scalar(select(func.count()).select_from(query.subquery()))
            books = session.scalars(query.order_by(desc(BookModel.created_at)).offset(offset).limit(limit)).all()
            
            result = {
                "items": books,
                "total": total,
                "limit": limit,
                "offset": offset,
                "keyword": keyword
            }
            
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error searching books by author: {e}")
            if 'session' in locals():
                session.close()
            return {
                "items": [],
                "total": 0,
                "limit": limit,
                "offset": offset,
                "keyword": keyword
            }
    
    def search_by_category(self, category: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Search books by category.
        
        Args:
            category: Category to search
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            Dict[str, Any]: Search results
        """
        try:
            session = self.SessionLocal()
            query = select(BookModel).filter(BookModel.category == category)
            
            total = session.scalar(select(func.count()).select_from(query.subquery()))
            books = session.scalars(query.order_by(desc(BookModel.created_at)).offset(offset).limit(limit)).all()
            
            result = {
                "items": books,
                "total": total,
                "limit": limit,
                "offset": offset
            }
            
            session.close()
            return result
        except Exception as e:
            logger.error(f"Error searching books by category: {e}")
            if 'session' in locals():
                session.close()
            return {
                "items": [],
                "total": 0,
                "limit": limit,
                "offset": offset
            } 