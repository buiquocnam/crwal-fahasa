from flask import Flask, render_template, request, jsonify
import requests
import logging
import time
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
API_URL = "http://api:8000"

# Initialize Flask
app = Flask(__name__)

def wait_for_api():
    """Wait for API to be available."""
    max_retries = 30
    retry_count = 0
    
    logger.info("Waiting for API to be available...")
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"{API_URL}/books", timeout=5)
            if response.status_code == 200:
                logger.info("API is available!")
                return True
        except requests.RequestException:
            pass
        
        retry_count += 1
        logger.info(f"API not available yet. Retry {retry_count}/{max_retries}")
        time.sleep(2)
    
    logger.error("Failed to connect to API")
    return False

@app.route('/')
def index():
    """Render the home page with search form."""
    return render_template('index.html')

@app.route('/search')
def search():
    """Handle search requests."""
    keyword = request.args.get('keyword', '')
    search_type = request.args.get('type', 'title')  # Default to title search
    page = request.args.get('page', 1, type=int)
    limit = 10
    offset = (page - 1) * limit
    
    if not keyword:
        return render_template('index.html', error="Từ khóa tìm kiếm không được để trống")
    
    try:
        # Choose the appropriate API endpoint based on search type
        if search_type == 'author':
            api_endpoint = f"{API_URL}/books/search/author"
        else:
            api_endpoint = f"{API_URL}/books/search/title"
        
        # Make API request
        response = requests.get(
            api_endpoint,
            params={"keyword": keyword, "limit": limit, "offset": offset}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Calculate pagination info
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
        else:
            error_message = f"API error: {response.status_code}"
            logger.error(error_message)
            return render_template('index.html', error=error_message)
    
    except requests.RequestException as e:
        error_message = f"Error connecting to API: {e}"
        logger.error(error_message)
        return render_template('index.html', error=error_message)

@app.route('/books')
def list_books():
    """List all books with pagination."""
    page = request.args.get('page', 1, type=int)
    limit = 10
    offset = (page - 1) * limit
    
    try:
        response = requests.get(
            f"{API_URL}/books",
            params={"limit": limit, "offset": offset}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Calculate pagination info
            total = data.get('total', 0)
            total_pages = (total + limit - 1) // limit if total > 0 else 0
            
            return render_template(
                'index.html',
                books=data.get('books', []),
                page=page,
                total_pages=total_pages,
                total=total,
                view_mode="all_books"
            )
        else:
            error_message = f"API error: {response.status_code}"
            logger.error(error_message)
            return render_template('index.html', error=error_message)
    
    except requests.RequestException as e:
        error_message = f"Error connecting to API: {e}"
        logger.error(error_message)
        return render_template('index.html', error=error_message)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Display book details."""
    try:
        response = requests.get(f"{API_URL}/books/{book_id}")
        
        if response.status_code == 200:
            book = response.json()
            return render_template('index.html', single_book=book, view_mode="book_detail")
        elif response.status_code == 404:
            return render_template('index.html', error=f"Không tìm thấy sách với ID {book_id}")
        else:
            error_message = f"API error: {response.status_code}"
            logger.error(error_message)
            return render_template('index.html', error=error_message)
    
    except requests.RequestException as e:
        error_message = f"Error connecting to API: {e}"
        logger.error(error_message)
        return render_template('index.html', error=error_message)

if __name__ == "__main__":
    # Wait for API to be available
    wait_for_api()
    
    # Start Flask
    app.run(host='0.0.0.0', port=8000, debug=False) 