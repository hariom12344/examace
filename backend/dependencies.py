"""
Authentication dependencies for FastAPI
"""
from typing import Optional
import sys
import logging
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User
from utils.jwt_utils import verify_token

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='auth_debug.log')
logger = logging.getLogger(__name__)

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user
    """
    # Extract Authorization header
    auth_header = request.headers.get("authorization")
    logger.info(f"[AUTH DEBUG] Authorization header: {auth_header[:50] if auth_header else 'NONE'}")
    
    if not auth_header:
        logger.info(f"[AUTH DEBUG] ERROR: No authorization header provided!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Parse Bearer token
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.info(f"[AUTH DEBUG] ERROR: Invalid authorization header format!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    logger.info(f"[AUTH DEBUG] Token received (first 50 chars): {token[:50]}")
    logger.info(f"[AUTH DEBUG] Token length: {len(token)}")
    
    # Verify token
    payload = verify_token(token)
    logger.info(f"[AUTH DEBUG] Payload after verify: {payload}")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user ID from token
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user

async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

async def get_optional_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency for optional authentication
    """
    auth_header = request.headers.get("authorization")
    if not auth_header:
        return None
    
    # Parse Bearer token
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    
    token = parts[1]
    payload = verify_token(token)
    
    if not payload:
        return None
    
    user_id: int = payload.get("sub")
    if not user_id:
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        return None
    
    return user
