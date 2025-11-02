# app/models/rate_limit_model.py
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from app.db.base import Base

class RateLimit(Base):
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    endpoint = Column(String)
    count = Column(Integer, default=0)
    last_request = Column(DateTime, default=datetime.utcnow)
