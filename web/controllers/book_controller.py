from flask import request, render_template
from models.book import Book

class BookController:
    def __init__(self, book_model: Book):
        self.book_model = book_model

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
            books=data.get('books', []),
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
            books=data.get('books', []),
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