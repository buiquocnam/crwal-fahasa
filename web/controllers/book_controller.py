from flask import request, render_template
from models.book import Book 
import requests
from typing import Optional, Dict, Any
from web.config.settings import API_URL, logger

class BookController:
    def __init__(self, book_model: Book):
        self.book_model = book_model
        self.api_url = API_URL

    def index(self) -> str:
        """Handle home page"""
        page = request.args.get('page', 1, type=int)
        limit = 10
        offset = (page - 1) * limit

        data = self.book_model.get_all_books(limit, offset)
        total = data.get('total', 0)
        total_pages = (total + limit - 1) // limit if total > 0 else 0

        return render_template(
            'index.html',
            books=data.get('items', []),
            page=page,
            total_pages=total_pages,
            total=total
        )

    def search(self) -> str:
        """Handle book search"""
        keyword = request.args.get('keyword', '')
        search_type = request.args.get('type', 'title')
        page = request.args.get('page', 1, type=int)
        limit = 10
        offset = (page - 1) * limit

        if not keyword:
            return render_template('index.html', error="Search keyword cannot be empty")

        data = self.book_model.search_books(keyword, search_type, limit, offset)
        total = data.get('total', 0)
        total_pages = (total + limit - 1) // limit if total > 0 else 0

        return render_template(
            'index.html',
            keyword=keyword,
            search_type=search_type,
            books=data.get('items', []),
            page=page,
            total_pages=total_pages,
            total=total
        )

    def book_detail(self, book_id: int) -> str:
        """Handle book detail page"""
        book = self.book_model.get_book_by_id(book_id)
        
        if book:
            return render_template('index.html', single_book=book, view_mode="book_detail")
        return render_template('index.html', error=f"Book with ID {book_id} not found")

    def get_books(self, page: int = 1, limit: int = 12, title: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all books with pagination and filtering.
        
        Args:
            page: Page number (1-based)
            limit: Items per page
            title: Filter by title
            category: Filter by category
            
        Returns:
            Dict[str, Any]: Dictionary containing books and pagination info
        """
        try:
            skip = (page - 1) * limit
            params = {
                "skip": skip,
                "limit": limit
            }
            if title:
                params["title"] = title
            if category:
                params["category"] = category
            
            response = requests.get(f"{self.api_url}/books/", params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                "books": [Book(**book) for book in data["items"]],
                "total": data["total"],
                "page": page,
                "total_pages": (data["total"] + limit - 1) // limit
            }
        except requests.RequestException as e:
            logger.error(f"Error getting books: {e}")
            return {
                "books": [],
                "total": 0,
                "page": page,
                "total_pages": 0,
                "error": "Error retrieving books"
            }
    
    def get_book(self, book_id: int) -> Optional[Book]:
        """
        Get book by ID.
        
        Args:
            book_id: Book ID
            
        Returns:
            Optional[Book]: Book if found, None otherwise
        """
        try:
            response = requests.get(f"{self.api_url}/books/{book_id}")
            response.raise_for_status()
            return Book(**response.json())
        except requests.RequestException as e:
            logger.error(f"Error getting book {book_id}: {e}")
            return None
    
    def search_books(self, keyword: str, search_type: str = "title", page: int = 1, limit: int = 12, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Search books.
        
        Args:
            keyword: Search keyword
            search_type: Type of search (title, author, category)
            page: Page number (1-based)
            limit: Items per page
            category: Filter by category
            
        Returns:
            Dict[str, Any]: Dictionary containing search results and pagination info
        """
        try:
            skip = (page - 1) * limit
            params = {
                "query": keyword,
                "search_type": search_type,
                "skip": skip,
                "limit": limit
            }
            if category:
                params["category"] = category
            
            response = requests.get(f"{self.api_url}/books/search/", params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                "books": [Book(**book) for book in data["items"]],
                "total": data["total"],
                "page": page,
                "total_pages": (data["total"] + limit - 1) // limit,
                "keyword": data["keyword"]
            }
        except requests.RequestException as e:
            logger.error(f"Error searching books: {e}")
            return {
                "books": [],
                "total": 0,
                "page": page,
                "total_pages": 0,
                "keyword": keyword,
                "error": "Error searching books"
            } 