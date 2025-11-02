from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class DomainAnalysis(Base):
    __tablename__ = "domain_analysis"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    total_results = Column(Integer)
    results = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
