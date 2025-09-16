"""
Database Configuration and Connection Management
"""
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import structlog

from app.config.settings import get_settings

settings = get_settings()
logger = structlog.get_logger(__name__)

# Create declarative base first
Base = declarative_base()

# Create async engine with SQLite-compatible settings
if "sqlite" in settings.DATABASE_URL:
    # SQLite configuration
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=10,
    )

# Create session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()

async def create_tables():
    """Create all database tables"""
    try:
        # Import all models to ensure they are registered with SQLAlchemy metadata
        from app.models import (
            User, Project, Requirement, Task, TaskDependency, TaskComment,
            AIAgent, AgentAction, AgentDecision, AgentWorkflow,
            AuditLog, SystemLog, SecurityEvent,
            Integration, IntegrationEvent, Deployment, DeploymentHealthCheck,
            Role, Permission, ProjectPermission, AgentPermission, SystemSetting
        )

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise

async def close_db_connection():
    """Close database connection"""
    try:
        await engine.dispose()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error("Error closing database connection", error=str(e))
