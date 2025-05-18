import requests
from typing import Dict, Optional
from config.settings import logger

class Book:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_all_books(self, limit: int = 10, offset: int = 0) -> Dict:
        """Get list of all books"""
        try:
            response = requests.get(
                f"{self.api_url}/books",
                params={"limit": limit, "offset": offset}
            )
            if response.status_code == 200:
                return response.json()
            return {"books": [], "total": 0}
        except requests.RequestException as e:
            logger.error(f"Error getting books: {e}")
            return {"books": [], "total": 0}

    def search_books(self, keyword: str, search_type: str = 'title', limit: int = 10, offset: int = 0) -> Dict:
        """Search books by keyword"""
        try:
            endpoint = f"{self.api_url}/books/search/{search_type}"
            response = requests.get(
                endpoint,
                params={"keyword": keyword, "limit": limit, "offset": offset}
            )
            if response.status_code == 200:
                return response.json()
            return {"books": [], "total": 0}
        except requests.RequestException as e:
            logger.error(f"Error searching books: {e}")
            return {"books": [], "total": 0}

    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        """Get book details by ID"""
        try:
            response = requests.get(f"{self.api_url}/books/{book_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException as e:
            logger.error(f"Error getting book details: {e}")
            return None 