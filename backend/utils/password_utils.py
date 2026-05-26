"""
Password hashing utilities
"""
from passlib.context import CryptContext

# Use pbkdf2 as primary since it's more stable
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using pbkdf2
    """
    return pwd_context.hash(password, scheme="pbkdf2_sha256")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)
