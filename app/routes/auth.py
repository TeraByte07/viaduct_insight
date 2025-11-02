from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.auth import UserCreate, UserLogin,RefreshTokenRequest, GenericResponseModel, UserResponse
from app.services.auth import UserService
from app.core.security import oauth2_scheme
from typing import Union

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    user_service = UserService(db)
    return user_service.create_user(user_data)

@router.post("/login")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.login(user_data)

@router.post("/logout", response_model=Union[GenericResponseModel, UserResponse])
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    service = UserService(db)
    return service.logout(token=token)

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.refresh_token(request.refresh_token)