from pydantic import BaseModel, EmailStr, Field
from typing import Optional, TypeVar, Generic
from uuid import UUID
from enum import Enum

class UserRole(str, Enum): 
    marketer = "marketer"
    seo = "seo"
    user = "user"

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Valid email address of the user")
    full_name: Optional[str] = Field(None, min_length=2, description="Full name of the user")
    role: Optional[UserRole] = Field(default=UserRole.user, description="User role (default: user)")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Valid email address of the user")
    password: str

class UserResponse(UserBase):
    user_id: UUID
    is_active: bool
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

    class Config:
        from_attributes = True

T = TypeVar('T')
class GenericResponseModel(BaseModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T] = None
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str