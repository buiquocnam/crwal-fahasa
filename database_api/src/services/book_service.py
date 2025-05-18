from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from ..repositories.book_repository import BookRepository
from ..models.book import BookCreate, Book, BookList, SearchResult, BatchBookResult
from database_api.src.config.settings import logger
 
class BookService:
    """Service for book business logic."""
    
    def __init__(self):
        """Initialize service."""
        self.repository = BookRepository()
    
    def get_books(self, skip: int = 0, limit: int = 100, title: Optional[str] = None, category: Optional[str] = None) -> BookList:
        """
        Get all books with pagination and filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            title: Filter by title
            category: Filter by category
            
        Returns:
            BookList: Paginated list of books
            
        Raises:
            HTTPException: If there's an error retrieving books
        """
        try:
            result = self.repository.get_all(limit=limit, offset=skip, title=title, category=category)
            return BookList(
                items=[Book.from_orm(book) for book in result["items"]],
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"]
            )
        except Exception as e:
            logger.error(f"Error getting books: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving books")
    
    def get_book(self, book_id: int) -> Book:
        """
        Get book by ID.
        
        Args:
            book_id: Book ID
            
        Returns:
            Book: Book data
            
        Raises:
            HTTPException: If book not found or error occurs
        """
        try:
            book = self.repository.get_by_id(book_id)
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")
            return Book.from_orm(book)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting book: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving book")

    def create_books(self, books_data: List[BookCreate]) -> BatchBookResult:
        """
        Create multiple books.
        
        Args:
            books_data: List of book data
            
        Returns:
            BatchBookResult: Results with success and error counts
            
        Raises:
            HTTPException: If all creations fail
        """
        try:
            result = self.repository.create_many([book.dict() for book in books_data])
            if result["success_count"] == 0:
                raise HTTPException(status_code=400, detail="Error creating books")
            return BatchBookResult(**result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating books: {e}")
            raise HTTPException(status_code=500, detail="Error creating books")
    
    
    def delete_all_books(self) -> Dict[str, int]:
        """
        Delete all books.
        
        Returns:
            Dict[str, int]: Number of deleted books
            
        Raises:
            HTTPException: If deletion fails
        """
        try:
            result = self.repository.delete_all()
            return result
        except Exception as e:
            logger.error(f"Error deleting all books: {e}")
            raise HTTPException(status_code=500, detail="Error deleting all books")
    
    def search_books(self, query: str, search_type: str = "title", skip: int = 0, limit: int = 100, category: Optional[str] = None) -> SearchResult:
        """
        Search books.
        
        Args:
            query: Search query
            search_type: Type of search (title, author, category)
            skip: Number of records to skip
            limit: Maximum number of records to return
            category: Filter by category
            
        Returns:
            SearchResult: Search results
            
        Raises:
            HTTPException: If search fails or invalid search type
        """
        try:
            if search_type == "title":
                result = self.repository.search_by_title(query, limit=limit, offset=skip, category=category)
            elif search_type == "author":
                result = self.repository.search_by_author(query, limit=limit, offset=skip, category=category)
            elif search_type == "category":
                result = self.repository.search_by_category(query, limit=limit, offset=skip)
            else:
                raise HTTPException(status_code=400, detail="Invalid search type")
            
            return SearchResult(
                items=[Book.from_orm(book) for book in result["items"]],
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
                keyword=result.get("keyword", query)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error searching books: {e}")
            raise HTTPException(status_code=500, detail="Error searching books") 