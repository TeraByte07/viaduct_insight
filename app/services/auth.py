from app.schemas.auth import UserCreate, UserResponse, UserLogin
from fastapi import HTTPException, status
from uuid import uuid4
from app.models.user_model import UserModel, BlacklistedToken
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, blacklist_token, get_current_user, is_token_blacklisted, verify_token
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import Optional


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def GenerateResponse(self, status_code: int, message: str, data: Optional[dict]=None):
        return JSONResponse(
            status_code = status_code,
            content = {
            "message": message,
            "data": data
            }
        )

    def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = self.db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if existing_user:
            return self.GenerateResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                message = "User with email already exists",
                data = None
            )

        hashed_password = hash_password(user_data.password)
        new_user = UserModel(
            user_id = uuid4(),
            full_name = user_data.full_name,
            email = user_data.email,
            hashed_password = hashed_password,
            role = user_data.role or "user"
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
    
        access_token = create_access_token({"sub": str(new_user.user_id)})
        refresh_token = create_refresh_token({"sub": str(new_user.user_id)})

        data = {
            "user_id": str(new_user.user_id),
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role.value if new_user.role else None,
            "is_active":new_user.is_active,
            "access_token": access_token,
            "refresh_token":refresh_token,
        }
        # Return response schema
        return self.GenerateResponse(
            status_code = status.HTTP_201_CREATED,
            message = "User registered successfully",
            data = data
        )

    def login(self, user_data: UserLogin) -> UserResponse:
        user = self.db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            return self.GenerateResponse(
                status_code = status.HTTP_401_UNAUTHORIZED,
                message = "Invalid email or password",
                data = None
            )
        access_token = create_access_token({"sub": str(user.user_id)})
        refresh_token = create_refresh_token({"sub": str(user.user_id)})

        return self.GenerateResponse(
            status_code = status.HTTP_200_OK,
            message = "Login successful",
            data = {
                "user_id": str(user.user_id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value if user.role else None,
                "is_active": user.is_active,
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
    def logout(self, token: str):
        current_user = get_current_user(token)
        if current_user is None:
            return self.GenerateResponse(
                status_code = status.HTTP_401_UNAUTHORIZED,
                message = "Invalid token",
                data = None
            )
        if is_token_blacklisted(self.db, token):
            return self.GenerateResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                message = "Token already blacklisted",
                data = None
            )
        try:
            self.db.add(BlacklistedToken(token=token))
            self.db.commit()
            return self.GenerateResponse(
                status_code = status.HTTP_200_OK,
                message = "Logout successful",
                data = None
            )
        except Exception as e:
            self.db.rollback()
            return self.GenerateResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Error logging out: {str(e)}"
            )
    
    def refresh_token(self, refresh_token: str):
        if is_token_blacklisted(self.db, refresh_token):
            return self.GenerateResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Refresh Token revoked!!"
            )
        try:
            payload = verify_token(refresh_token)
        except HTTPException as e:
            return self.GenerateResponse(
                status_code=e.status_code,
                message=e.detail
            )
        if payload.get("type") != "refresh":
            return self.GenerateResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Provided token is not a refresh token."
            )
        user_id = payload.get("sub")
        if not user_id:
            return self.GenerateResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Token missing subject."
            )
            
        user = self.db.query(UserModel).filter(UserModel.user_id == user_id if isinstance(user_id, str) else user_id).first()
        if not user:
            return self.GenerateResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="User not found for token subject."
            )

        try:
            if not is_token_blacklisted(self.db, refresh_token):
                self.db.add(BlacklistedToken(token=refresh_token))
                self.db.commit()
            # create new tokens
            new_access_token = create_access_token({"sub": str(user.user_id)})
            new_refresh_token = create_refresh_token({"sub": str(user.user_id)})
            return self.GenerateResponse(
                status_code=status.HTTP_200_OK,
                message="New tokens generated",
                data={
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                    "token_type": "bearer"
                }
            )
        except Exception as e:
            self.db.rollback()
            return self.GenerateResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to rotate refresh token"
            )