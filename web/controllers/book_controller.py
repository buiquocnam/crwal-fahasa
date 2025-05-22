from flask import request, render_template, redirect, url_for, abort, session
from models.book import Book 
from typing import Optional, Dict, Any
from config.settings import API_URL, logger

class BookController:
    def __init__(self, book_model: Book):
        self.book_model = book_model
        self.api_url = API_URL

    def index(self) -> str:
        """Xử lý trang chủ"""
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 15, type=int)
        category = request.args.get('category', None)
        
        # Lấy danh sách sách từ API
        data = self.book_model.get_books(
            limit=limit, 
            page=page,
            category=category
        )
        
        # Lấy danh sách sách
        books = data.get('items', [])
        
        # Lấy danh mục phổ biến
        categories = self.book_model.get_categories()
        
        # Dữ liệu cho template
        template_data = {
            'books': books,
            'page': page,
            'total_pages': data.get('total_pages', 0),
            'total': data.get('total', 0),
            'category': category,
            'search_type': 'title',  # Giá trị mặc định cho search_type
            'view_mode': 'home-page',  # Đánh dấu là trang chủ
            'categories': categories  # Thêm danh mục vào dữ liệu
        }
        
      
        return render_template('index.html', **template_data)

    def search(self) -> str:
        """Xử lý tìm kiếm sách"""
        keyword = request.args.get('keyword', '')
        search_type = request.args.get('search_type', 'title')  # title, author, category
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 15, type=int)
        category = request.args.get('category', None)
        
        # Bỏ đoạn kiểm tra và redirect khi không có từ khóa/category
        # JavaScript sẽ xử lý thông báo toast
        
        # Lấy dữ liệu sách từ API thống nhất
        data = self.book_model.get_books(
            limit=limit, 
            page=page, 
            keyword=keyword, 
            search_type=search_type,
            category=category
        )
        
        # Lấy danh sách sách
        books = data.get('items', [])
        
        # Dữ liệu cho template
        template_data = {
            'keyword': keyword,
            'search_type': search_type,
            'category': category,
            'books': books,
            'page': data.get('page', page),
            'total_pages': data.get('total_pages', 0),
            'total': data.get('total', 0),
            'view_mode': 'search'  # Đảm bảo luôn có view_mode để hiển thị đúng
        }
        
        # Kiểm tra nếu không có kết quả tìm kiếm
        if not books and keyword:
            template_data['error'] = f'Không tìm thấy kết quả nào cho "{keyword}"'
        
        # Kiểm tra nếu yêu cầu là AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render_template('partials/book_list.html', **template_data)
        else:
            return render_template('index.html', **template_data)

    def book_detail(self, book_id: int) -> str:
        """Xử lý trang chi tiết sách"""
        book = self.book_model.get_book_by_id(book_id)
        
        if not book:
            abort(404, description=f"Không tìm thấy sách với ID {book_id}")
            
        # Render template với dữ liệu chi tiết sách
        return render_template('index.html', single_book=book, view_mode="book_detail")

    def categories(self) -> str:
        """Xử lý hiển thị danh sách danh mục sách"""
        # Lấy danh sách danh mục từ API
        categories = self.book_model.get_categories()
        
        # Render template với dữ liệu danh mục
        return render_template('index.html', categories=categories, view_mode="categories") 