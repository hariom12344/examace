"""
JWT Token utilities for authentication
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='jwt_debug.log')
logger = logging.getLogger(__name__)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    """
    to_encode = data.copy()
    
    # PyJWT v2.0+ requires 'sub' claim to be a string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token
    """
    to_encode = data.copy()
    
    # PyJWT v2.0+ requires 'sub' claim to be a string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode JWT token
    """
    try:
        logger.info(f"[JWT] Attempting to verify token (first 50 chars): {token[:50]}")
        logger.info(f"[JWT] SECRET_KEY: {settings.SECRET_KEY[:20]}...")
        logger.info(f"[JWT] ALGORITHM: {settings.ALGORITHM}")
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Convert sub back to integer since it was stored as string in JWT
        if "sub" in payload:
            try:
                payload["sub"] = int(payload["sub"])
            except (ValueError, TypeError):
                pass  # Keep as string if conversion fails
        
        logger.info(f"[JWT] ✓ Token verified successfully. Payload: {payload}")
        print(f"[JWT DEBUG] Token verified successfully. Sub: {payload.get('sub')}")
        return payload
    except jwt.ExpiredSignatureError as e:
        logger.error(f"[JWT] ✗ Token expired: {e}")
        print(f"[JWT DEBUG] Token expired: {e}")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"[JWT] ✗ Invalid token: {type(e).__name__}: {e}")
        print(f"[JWT DEBUG] Invalid token: {e}")
        return None
    except Exception as e:
        logger.error(f"[JWT] ✗ Unexpected error: {type(e).__name__}: {e}")
        print(f"[JWT DEBUG] Unexpected error: {e}")
        return None

def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Get payload from token without verification (for error checking)
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True}
        )
        return payload
    except:
        return None
