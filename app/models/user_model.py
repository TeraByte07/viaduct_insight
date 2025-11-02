from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from app.db.base import Base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.sql import func
from app.db.base import Base
import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class UserRole(enum.Enum):
    marketer = "marketer"
    seo = "seo"
    admin = "admin"
    user = "user"

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.marketer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    token = Column(String, primary_key=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)