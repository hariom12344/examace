"""
Routers package
"""
from .auth import router as auth_router
from . import exam, question, result, analytics

__all__ = ["auth_router", "exam", "question", "result", "analytics"]
