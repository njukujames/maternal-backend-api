"""
Database Configuration and Session Management
Provides SQLAlchemy engine, session factory, and dependency injection for FastAPI
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/maternal_health_db")

# Create SQLAlchemy engine
# For PostgreSQL production
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=20,  # Maximum overflow connections
    echo=False  # Set to True for SQL query logging during development
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI endpoints
    Provides a database session and ensures it's closed after use
    
    Usage in FastAPI endpoint:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    Should only be used for testing or initial setup
    In production, use Alembic migrations instead
    """
    from app.db.models import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_db():
    """
    Drop all database tables
    WARNING: This will delete all data!
    Only use in development/testing
    """
    from app.db.models import Base
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")