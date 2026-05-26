"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserResponse, LoginResponse, TokenResponse
from utils import create_access_token, create_refresh_token, verify_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    User signup endpoint
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_password,
        role="student"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate tokens
    access_token = create_access_token(data={"sub": new_user.id})
    refresh_token = create_refresh_token(data={"sub": new_user.id})
    
    return {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "role": new_user.role,
        "is_active": new_user.is_active,
        "created_at": new_user.created_at,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 1800  # 30 minutes
    }

@router.post("/login", response_model=LoginResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 1800  # 30 minutes
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: dict, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    """
    refresh_token_str = data.get("refresh_token")
    
    if not refresh_token_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )
    
    # Verify refresh token
    payload = verify_token(refresh_token_str)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user_id = payload.get("sub")
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new access token
    new_access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 1800
    }

@router.post("/logout")
async def logout():
    """
    Logout endpoint (token invalidation handled on client side)
    """
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = None
):
    """
    Get current authenticated user info
    """
    # This will be protected by JWT dependency in actual implementation
    return current_user
