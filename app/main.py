"""
Maternal Health Monitoring App - FastAPI Main Application
MVP v1.0 - Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI(
    title="Maternal Health Monitoring API",
    description="API for tracking maternal health metrics during first trimester",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API is running.
    Returns status 200 with success message.
    """
    return {
        "status": "healthy",
        "message": "Maternal Health Monitoring API is running",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with basic API information.
    """
    return {
        "message": "Welcome to Maternal Health Monitoring API",
        "docs": "/api/docs",
        "health": "/health"
    }

# TODO: Import and include routers when implemented
# from app.routers import auth, users, logs, content, feedback
# app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/v1/users", tags=["Users"])
# app.include_router(logs.router, prefix="/v1/logs", tags=["Daily Logs"])
# app.include_router(content.router, prefix="/v1/content", tags=["Content"])
# app.include_router(feedback.router, prefix="/v1/feedback", tags=["Feedback"])