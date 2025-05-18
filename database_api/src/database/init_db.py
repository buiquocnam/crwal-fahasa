from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
import time
from typing import Generator
from database_api.src.config.settings import DATABASE_URL, logger

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, 
    pool_recycle=3600,   
    pool_size=5,         
    max_overflow=10,    
    pool_timeout=30      
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> bool:
    """
    Initialize database tables with retry mechanism.
    
    Returns:
        bool: True if successful, False otherwise
    """
    max_retries = 5
    retry_interval = 3
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to initialize database (attempt {attempt + 1}/{max_retries})")
            
            # Test database connection
            with engine.connect() as conn:
                logger.info("Database connection successful")
            
            # Import models here to ensure they are registered with Base
            from database_api.src.models.book import BookModel
            
            # Drop all tables and recreate them
            Base.metadata.drop_all(bind=engine)
            logger.info("Dropped existing tables")
            
            # Create tables
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing database (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                logger.warning(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logger.error(f"Failed to initialize database after {max_retries} attempts")
                return False
    
    return False

# Initialize database on module import
try:
    if init_db():
        logger.info("Database initialized successfully")
    else:
        logger.error("Failed to initialize database")
except Exception as e:
    logger.error(f"Unexpected error during database initialization: {str(e)}")

