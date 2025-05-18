import os
import logging
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API configuration
API_URL = os.environ.get("API_URL", "http://fahasa_api:8000")

# Flask configuration
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.environ.get("FLASK_PORT", 8000))
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

# Pagination configuration
DEFAULT_PAGE_SIZE = 10 