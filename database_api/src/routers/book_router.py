from typing import List, Optional
from fastapi import APIRouter, Query, Path
from ..services.book_service import BookService
from ..models.book import BookCreate, Book, BookList, BatchBookResult

router = APIRouter(
    prefix="/books", 
    tags=["books"],
    responses={404: {"description": "Không tìm thấy sách"}}
)

book_service = BookService()

@router.get("/", response_model=BookList)
async def get_books(
    limit: int = Query(100, ge=1, le=100, description="Số lượng bản ghi tối đa trả về"),
    page: int = Query(1, ge=1, description="Số trang hiện tại"),
    keyword: Optional[str] = Query(None, description="Từ khóa tìm kiếm (nếu có)"),
    search_type: str = Query("title", description="Loại tìm kiếm (title, author, category)"),
    category: Optional[str] = Query(None, description="Lọc theo danh mục")
):
    """
    Lấy danh sách tất cả sách hoặc tìm kiếm sách với phân trang và lọc.
    
    Tham số:
        limit: Số lượng bản ghi tối đa trả về
        page: Số trang hiện tại
        keyword: Từ khóa tìm kiếm (nếu có) 
        search_type: Loại tìm kiếm (title, author, category)
        category: Lọc theo danh mục
        
    Trả về:
        BookList: Danh sách sách đã phân trang
    """
    return book_service.get_books(
        limit=limit, 
        page=page, 
        keyword=keyword, 
        search_type=search_type, 
        category=category
    )

@router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: int = Path(..., ge=1, description="ID sách")
):
    """
    Lấy thông tin sách theo ID.
    
    Tham số:
        book_id: ID sách
        
    Trả về:
        Book: Thông tin sách
    """
    return book_service.get_book(book_id)

@router.post("/batch", response_model=BatchBookResult)
async def create_books(books_data: List[BookCreate]):
    """
    Tạo nhiều sách cùng lúc.
    
    Tham số:
        books_data: Danh sách thông tin sách
        
    Trả về:
        BatchBookResult: Kết quả với số lượng thành công và thất bại
    """
    return book_service.create_books(books_data)


@router.delete("/deleteAll", response_model=dict)
async def delete_all_books():
    """
    Xóa tất cả sách.
    
    Trả về:
        Dict[str, int]: Số lượng sách đã xóa
    """
    return book_service.delete_all_books()

@router.get("/categories/list", response_model=List[str])
async def get_categories():
    """
    Lấy danh sách tất cả các danh mục sách.
    
    Trả về:
        List[str]: Danh sách các danh mục sách
    """
    return book_service.get_categories()