from typing import List, Optional
from fastapi import APIRouter, Query, Path
from ..services.book_service import BookService
from ..models.book import BookCreate, Book, BookList, SearchResult, BatchBookResult

router = APIRouter(
    prefix="/books", 
    tags=["books"],
    responses={404: {"description": "Không tìm thấy sách"}}
)

book_service = BookService()

@router.get("/", response_model=BookList)
async def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    title: Optional[str] = Query(None, description="Filter by title"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Get all books with pagination and filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        title: Filter by title
        category: Filter by category
        
    Returns:
        BookList: Paginated list of books
    """
    return book_service.get_books(skip=skip, limit=limit, title=title, category=category)

@router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: int = Path(..., ge=1, description="Book ID")
):
    """
    Get book by ID.
    
    Args:
        book_id: Book ID
        
    Returns:
        Book: Book data
    """
    return book_service.get_book(book_id)

@router.post("/batch", response_model=BatchBookResult)
async def create_books(books_data: List[BookCreate]):
    """
    Create multiple books.
    
    Args:
        books_data: List of book data
        
    Returns:
        BatchBookResult: Results with success and error counts
    """
    return book_service.create_books(books_data)


@router.delete("/deleteAll", response_model=dict)
async def delete_all_books():
    """
    Delete all books.
    
    Returns:
        Dict[str, int]: Number of deleted books
    """
    return book_service.delete_all_books()

@router.get("/search/{search_type}", response_model=SearchResult)
async def search_books(
    search_type: str = Path(..., description="Type of search (title, author, category)"),
    keyword: str = Query(..., description="Search keyword"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Search books.
    
    Args:
        search_type: Type of search (title, author, category)
        keyword: Search keyword
        limit: Maximum number of records to return
        offset: Number of records to skip
        category: Filter by category
        
    Returns:
        SearchResult: Search results
    """
    return book_service.search_books(
        query=keyword,
        search_type=search_type,
        skip=offset,
        limit=limit,
        category=category
    ) 