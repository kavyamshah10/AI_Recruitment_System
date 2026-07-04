"""
database.py
-------------------------
Creates the PostgreSQL database connection using SQLAlchemy.
This file is imported by every module that needs database access.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """
    Returns a database session.

    Usage:
        db = get_db()

        # Perform database operations

        db.close()
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()