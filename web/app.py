from flask import Flask
from config.settings import API_URL, FLASK_HOST, FLASK_PORT, FLASK_DEBUG
from models.book import Book
from controllers.book_controller import BookController
from utils.api_utils import wait_for_api

def create_app():
    """Initialize and configure Flask application"""
    app = Flask(__name__)
    
    # Initialize model and controller
    book_model = Book(API_URL)
    book_controller = BookController(book_model)
    
    # Register routes
    @app.route('/')
    def index():
        return book_controller.index()
    
    @app.route('/search')
    def search():
        return book_controller.search()
    
    @app.route('/book/<int:book_id>')
    def book_detail(book_id):
        return book_controller.book_detail(book_id)
    
    return app

if __name__ == "__main__":
    # Wait for API to be ready
    if wait_for_api(API_URL):
        # Initialize and run application
        app = create_app()
        app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
    else:
        print("Failed to start application: API is not available") 