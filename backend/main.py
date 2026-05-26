"""
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from routers import auth_router
from routers import exam, question, result, analytics
from database import Base, engine

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[STARTUP] ExamAce Backend Starting...")
    print(f"[DATABASE] {settings.DATABASE_URL}")
    print("[SECURITY] JWT Authentication Enabled")
    yield
    # Shutdown
    print("[SHUTDOWN] ExamAce Backend Shutting Down...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Competitive Exam Platform",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS Middleware - MUST be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/")
async def root():
    return {
        "message": "Welcome to ExamAce Backend",
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "database": "connected"
    }

@app.get("/debug/test")
async def test_endpoint():
    return {
        "message": "Test endpoint working",
        "status": "ok"
    }

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(exam.router, prefix="/api")
app.include_router(question.router, prefix="/api")
app.include_router(result.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
