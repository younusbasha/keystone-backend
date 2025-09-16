"""
Search Functionality Endpoints
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.search import (
    SearchRequest, SearchResponse, GlobalSearchResponse
)
from app.services.search_service import search_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=SearchResponse)
async def search_all(
    q: str = Query(..., min_length=1, description="Search query"),
    category: Optional[str] = Query(None, description="Search category filter"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Search across all entities"""
    results = await search_service.search_all(db, q, current_user.id, category, skip, limit)
    return results

@router.get("/projects", response_model=SearchResponse)
async def search_projects(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Search projects"""
    results = await search_service.search_projects(db, q, current_user.id, skip, limit)
    return results

@router.get("/requirements", response_model=SearchResponse)
async def search_requirements(
    q: str = Query(..., min_length=1, description="Search query"),
    project_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Search requirements"""
    results = await search_service.search_requirements(db, q, current_user.id, project_id, skip, limit)
    return results

@router.get("/tasks", response_model=SearchResponse)
async def search_tasks(
    q: str = Query(..., min_length=1, description="Search query"),
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Search tasks"""
    results = await search_service.search_tasks(db, q, current_user.id, project_id, status, skip, limit)
    return results

@router.get("/agents", response_model=SearchResponse)
async def search_agents(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Search AI agents"""
    results = await search_service.search_agents(db, q, current_user.id, skip, limit)
    return results

@router.get("/global", response_model=GlobalSearchResponse)
async def global_search(
    q: str = Query(..., min_length=1, description="Global search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Global search across all entities with categorized results"""
    results = await search_service.global_search(db, q, current_user.id, skip, limit)
    return results
