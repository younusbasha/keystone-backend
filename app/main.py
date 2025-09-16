"""
TechSophy Keystone - AI-Powered SDLC Management Platform
FastAPI Application Main Entry Point
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from app.config.settings import get_settings
from app.config.database import create_tables, close_db_connection
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware
from app.core.exceptions import (
    ValidationException,
    AuthenticationException,
    AuthorizationException,
    NotFoundException,
    ConflictException,
    InternalServerException,
)
from app.api.v1.router import api_router
from app.utils.helpers import setup_logging
# Import models to ensure they are registered with SQLAlchemy
import app.models

settings = get_settings()
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await create_tables()
    yield
    # Shutdown
    await close_db_connection()

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="""
    TechSophy Keystone is an AI-Powered Software Development Lifecycle (SDLC) 
    Management Platform that automates the entire software development process 
    using intelligent AI agents.
    
    ## Features
    - User authentication and authorization
    - Project management with full CRUD operations
    - Requirements management with AI analysis
    - Task generation from requirements
    - Real-time collaboration features
    
    ## Authentication
    Use the `/auth/login` endpoint to get an access token, then include it in the Authorization header:
    `Authorization: Bearer <your_access_token>`
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)

# Global exception handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Input validation failed",
            "details": exc.errors()
        }
    )

@app.exception_handler(ValidationException)
async def custom_validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation Error",
            "message": str(exc),
            "details": exc.details if hasattr(exc, 'details') else None
        }
    )

@app.exception_handler(AuthenticationException)
async def authentication_exception_handler(request: Request, exc: AuthenticationException):
    return JSONResponse(
        status_code=401,
        content={
            "error": "Authentication Error",
            "message": str(exc)
        }
    )

@app.exception_handler(AuthorizationException)
async def authorization_exception_handler(request: Request, exc: AuthorizationException):
    return JSONResponse(
        status_code=403,
        content={
            "error": "Authorization Error",
            "message": str(exc)
        }
    )

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": str(exc)
        }
    )

@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=409,
        content={
            "error": "Conflict",
            "message": str(exc)
        }
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Database Integrity Error",
            "message": "The operation violates database constraints"
        }
    )

@app.exception_handler(InternalServerException)
async def internal_server_exception_handler(request: Request, exc: InternalServerException):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )

# CORS middleware
cors_origins = []
if settings.BACKEND_CORS_ORIGINS:
    cors_origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Allow all origins in development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, calls=settings.RATE_LIMIT_PER_MINUTE, period=60)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
        "docs_url": "/docs" if settings.ENVIRONMENT != "production" else None,
        "openapi_url": f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
        "endpoints": {
            "authentication": f"{settings.API_V1_STR}/auth",
            "projects": f"{settings.API_V1_STR}/projects",
            "requirements": f"{settings.API_V1_STR}/requirements"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
