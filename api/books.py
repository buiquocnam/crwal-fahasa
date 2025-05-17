from fastapi import APIRouter, HTTPException, Query, Depends, Body, Response
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from database import get_db, BookDB
from models import Book, BookList, SearchResult, BookCreate, BatchBookResult
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
    category: Optional[str] = Query(None, description="Lọc theo danh mục"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Lấy tất cả sách với phân trang và lọc theo tiêu đề, danh mục (nếu có)."""
    try:
        # Xây dựng query
        query = db.query(BookDB)
        
        if title:
            query = query.filter(BookDB.title.ilike(f"%{title}%"))
            
        if category:
            query = query.filter(BookDB.category == category)
        
        # Lấy tổng số sách
        total = query.count()
        
        # Thực hiện phân trang
        books = query.order_by(BookDB.id).offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "books": books
        }
    
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách sách: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Lấy sách cụ thể theo ID."""
    try:
        book = db.query(BookDB).filter(BookDB.id == book_id).first()
        
        if not book:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy sách với ID {book_id}")
        
        return book
    
    except Exception as e:
        logger.error(f"Lỗi khi lấy sách {book_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookCreate = Body(...), db: Session = Depends(get_db)):
    """Thêm một cuốn sách mới vào database."""
    try:
        db_book = BookDB(
            title=book.title,
            price=book.price,
            original_price=book.original_price,
            discount=book.discount,
            image_url=book.image_url,
            product_code=book.product_code,
            supplier=book.supplier,
            author=book.author,
            publisher=book.publisher,
            publish_year=book.publish_year,
            weight=book.weight,
            dimensions=book.dimensions,
            page_count=book.page_count,
            cover_type=book.cover_type,
            url=book.url,
            description=book.description,
            category=book.category,
            language=book.language
        )
        
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        
        logger.info(f"Đã thêm sách mới: {book.title}")
        return db_book
            
    except Exception as e:
        db.rollback()
        logger.error(f"Lỗi khi thêm sách mới: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=BatchBookResult, status_code=201)
async def create_books_batch(books: List[BookCreate] = Body(...), db: Session = Depends(get_db)):
    """Thêm nhiều cuốn sách vào database cùng lúc."""
    success_count = 0
    failed_count = 0
    failed_books = []

    try:
        for book in books:
            try:
                db_book = BookDB(
                    title=book.title,
                    price=book.price,
                    original_price=book.original_price,
                    discount=book.discount,
                    image_url=book.image_url,
                    product_code=book.product_code,
                    supplier=book.supplier,
                    author=book.author,
                    publisher=book.publisher,
                    publish_year=book.publish_year,
                    weight=book.weight,
                    dimensions=book.dimensions,
                    page_count=book.page_count,
                    cover_type=book.cover_type,
                    url=book.url,
                    description=book.description,
                    category=book.category,
                    language=book.language
                )
                
                db.add(db_book)
                success_count += 1
            except Exception as e:
                failed_count += 1
                failed_books.append({"title": book.title, "error": str(e)})
                logger.error(f"Lỗi khi thêm sách '{book.title}': {e}")
        
        # Chỉ commit khi có sách thành công
        if success_count > 0:
            db.commit()
            
        logger.info(f"Đã thêm {success_count}/{len(books)} sách thành công")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Lỗi khi thêm nhiều sách: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "total": len(books),
        "success_count": success_count,
        "failed_count": failed_count,
        "failed_items": failed_books
    }

@router.get("/search/title", response_model=SearchResult)
async def search_books_by_title(
    keyword: str = Query(..., description="Từ khóa tìm kiếm trong tiêu đề sách"),
    limit: int = Query(DEFAULT_LIMIT, description="Số lượng sách trả về", ge=1, le=MAX_LIMIT),
    offset: int = Query(0, description="Số lượng sách bỏ qua", ge=0),
    category: Optional[str] = Query(None, description="Lọc kết quả theo danh mục"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Tìm kiếm sách theo từ khóa trong tiêu đề."""
    try:
        # Xây dựng query
        query = db.query(BookDB).filter(BookDB.title.ilike(f"%{keyword}%"))
        
        if category:
            query = query.filter(BookDB.category == category)
        
        # Lấy tổng số kết quả
        total = query.count()
        
        # Lấy sách phù hợp với phân trang
        books = query.order_by(BookDB.id).offset(offset).limit(limit).all()
        
        return {
            "keyword": keyword,
            "total": total,
            "limit": limit,
            "offset": offset,
            "books": books
        }
    
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm sách với từ khóa '{keyword}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/author", response_model=SearchResult)
async def search_books_by_author(
    keyword: str = Query(..., description="Từ khóa tìm kiếm trong tên tác giả"),
    limit: int = Query(DEFAULT_LIMIT, description="Số lượng sách trả về", ge=1, le=MAX_LIMIT),
    offset: int = Query(0, description="Số lượng sách bỏ qua", ge=0),
    category: Optional[str] = Query(None, description="Lọc kết quả theo danh mục"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Tìm kiếm sách theo từ khóa trong tên tác giả."""
    try:
        # Xây dựng query
        query = db.query(BookDB).filter(BookDB.author.ilike(f"%{keyword}%"))
        
        if category:
            query = query.filter(BookDB.category == category)
        
        # Lấy tổng số kết quả
        total = query.count()
        
        # Lấy sách phù hợp với phân trang
        books = query.order_by(BookDB.id).offset(offset).limit(limit).all()
        
        return {
            "keyword": keyword,
            "total": total,
            "limit": limit,
            "offset": offset,
            "books": books
        }
    
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm sách với tác giả '{keyword}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/category", response_model=BookList)
async def search_books_by_category(
    category: str = Query(..., description="Danh mục sách cần tìm"),
    limit: int = Query(DEFAULT_LIMIT, description="Số lượng sách trả về", ge=1, le=MAX_LIMIT),
    offset: int = Query(0, description="Số lượng sách bỏ qua", ge=0),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Tìm kiếm sách theo danh mục."""
    try:
        # Xây dựng query
        query = db.query(BookDB).filter(BookDB.category == category)
        
        # Lấy tổng số kết quả
        total = query.count()
        
        # Lấy sách phù hợp với phân trang
        books = query.order_by(BookDB.id).offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "books": books
        }
    
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm sách theo danh mục '{category}': {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
    
@router.delete("/deleteAll", status_code=200)
async def delete_all_books(db: Session = Depends(get_db)):
    """Xóa tất cả sách từ database."""
    try:
        # Đếm số lượng sách trước khi xóa
        count = db.query(BookDB).count()
        
        # Xóa tất cả sách
        db.query(BookDB).delete()
        db.commit()
        
        logger.info(f"Đã xóa tất cả {count} sách từ database")
        
        return {
            "success": True,
            "message": f"Đã xóa thành công {count} sách từ database",
            "count": count
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Lỗi khi xóa tất cả sách: {e}")
        raise HTTPException(status_code=500, detail=str(e))