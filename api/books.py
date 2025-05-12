from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Dict, Any, Optional
import psycopg2
from database import get_db
from models import Book, BookList, SearchResult
from config import DEFAULT_LIMIT, MAX_LIMIT, logger

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Không tìm thấy sách"}},
)

@router.get("/", response_model=BookList)
async def get_books(
    limit: int = Query(DEFAULT_LIMIT, description="Số lượng sách trả về", ge=1, le=MAX_LIMIT),
    offset: int = Query(0, description="Số lượng sách bỏ qua", ge=0),
    title: Optional[str] = Query(None, description="Lọc theo tiêu đề"),
    conn = Depends(get_db)
) -> Dict[str, Any]:
    """Lấy tất cả sách với phân trang và lọc theo tiêu đề (nếu có)."""
    try:
        with conn.cursor() as cursor:
            # Xây dựng câu truy vấn dựa trên tham số lọc
            query = "SELECT * FROM books"
            count_query = "SELECT COUNT(*) FROM books"
            params = []
            
            if title:
                query += " WHERE title ILIKE %s"
                count_query += " WHERE title ILIKE %s"
                params.append(f"%{title}%")
                
            query += " ORDER BY id LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # Thực thi truy vấn
            cursor.execute(query, params)
            books = cursor.fetchall()
            
            # Lấy tổng số sách
            cursor.execute(count_query, params[:-2] if params else [])
            total = cursor.fetchone()["count"]
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "books": list(books)
        }
    
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách sách: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, conn = Depends(get_db)) -> Dict[str, Any]:
    """Lấy sách cụ thể theo ID."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM books WHERE id = %s",
                (book_id,)
            )
            book = cursor.fetchone()
        
        if not book:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy sách với ID {book_id}")
        
        return book
    
    except psycopg2.Error as e:
        logger.error(f"Lỗi cơ sở dữ liệu khi lấy sách {book_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/title", response_model=SearchResult)
async def search_books_by_title(
    keyword: str = Query(..., description="Từ khóa tìm kiếm trong tiêu đề sách"),
    limit: int = Query(DEFAULT_LIMIT, description="Số lượng sách trả về", ge=1, le=MAX_LIMIT),
    offset: int = Query(0, description="Số lượng sách bỏ qua", ge=0),
    conn = Depends(get_db)
) -> Dict[str, Any]:
    """Tìm kiếm sách theo từ khóa trong tiêu đề."""
    try:
        with conn.cursor() as cursor:
            search_pattern = f"%{keyword}%"
            
            # Lấy sách phù hợp
            cursor.execute(
                "SELECT * FROM books WHERE title ILIKE %s ORDER BY id LIMIT %s OFFSET %s",
                (search_pattern, limit, offset)
            )
            books = cursor.fetchall()
            
            # Lấy tổng số kết quả phù hợp
            cursor.execute(
                "SELECT COUNT(*) FROM books WHERE title ILIKE %s",
                (search_pattern,)
            )
            total = cursor.fetchone()["count"]
        
        return {
            "keyword": keyword,
            "total": total,
            "limit": limit,
            "offset": offset,
            "books": list(books)
        }
    
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm sách với từ khóa '{keyword}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/author", response_model=SearchResult)
async def search_books_by_author(
    keyword: str = Query(..., description="Từ khóa tìm kiếm trong tên tác giả"),
    limit: int = Query(DEFAULT_LIMIT, description="Số lượng sách trả về", ge=1, le=MAX_LIMIT),
    offset: int = Query(0, description="Số lượng sách bỏ qua", ge=0),
    conn = Depends(get_db)
) -> Dict[str, Any]:
    """Tìm kiếm sách theo từ khóa trong tên tác giả."""
    try:
        with conn.cursor() as cursor:
            search_pattern = f"%{keyword}%"
            
            # Lấy sách phù hợp
            cursor.execute(
                "SELECT * FROM books WHERE author ILIKE %s ORDER BY id LIMIT %s OFFSET %s",
                (search_pattern, limit, offset)
            )
            books = cursor.fetchall()
            
            # Lấy tổng số kết quả phù hợp
            cursor.execute(
                "SELECT COUNT(*) FROM books WHERE author ILIKE %s",
                (search_pattern,)
            )
            total = cursor.fetchone()["count"]
        
        return {
            "keyword": keyword,
            "total": total,
            "limit": limit,
            "offset": offset,
            "books": list(books)
        }
    
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm sách với tác giả '{keyword}': {e}")
        raise HTTPException(status_code=500, detail=str(e)) 