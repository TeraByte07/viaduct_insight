from sqlalchemy.orm import sessionmaker
from functools import lru_cache
from app.core.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()