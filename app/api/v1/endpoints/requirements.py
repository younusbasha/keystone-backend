"""
Requirements Management Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.requirement import (
    RequirementCreate, RequirementUpdate, RequirementResponse,
    RequirementAnalysis, RequirementStatusUpdate, RequirementHistory,
    RequirementApproval
)
from app.services.requirement_service import requirement_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=RequirementResponse, status_code=status.HTTP_201_CREATED)
async def create_requirement(
    requirement_data: RequirementCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new requirement"""
    requirement = await requirement_service.create_requirement(db, requirement_data, current_user.id)
    return RequirementResponse.from_orm(requirement)

@router.get("/", response_model=List[RequirementResponse])
async def get_requirements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all requirements"""
    requirements = await requirement_service.get_requirements(db, current_user.id, skip, limit)
    return requirements

@router.get("/{requirement_id}", response_model=RequirementResponse)
async def get_requirement(
    requirement_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get requirement by ID"""
    requirement = await requirement_service.get_requirement_by_id(db, requirement_id, current_user.id)
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return RequirementResponse.from_orm(requirement)

@router.put("/{requirement_id}", response_model=RequirementResponse)
async def update_requirement(
    requirement_id: int,
    requirement_data: RequirementUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update requirement"""
    requirement = await requirement_service.update_requirement(db, requirement_id, requirement_data, current_user.id)
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return RequirementResponse.from_orm(requirement)

@router.delete("/{requirement_id}")
async def delete_requirement(
    requirement_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete requirement"""
    success = await requirement_service.delete_requirement(db, requirement_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return {"message": "Requirement deleted successfully"}

@router.get("/project/{project_id}", response_model=List[RequirementResponse])
async def get_project_requirements(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get requirements for a specific project"""
    requirements = await requirement_service.get_project_requirements(db, project_id, current_user.id, skip, limit)
    return requirements

@router.post("/{requirement_id}/analyze", response_model=RequirementAnalysis)
async def analyze_requirement(
    requirement_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Analyze requirement using AI"""
    analysis = await requirement_service.analyze_requirement(db, requirement_id, current_user.id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found or analysis failed"
        )
    return analysis

@router.post("/analyze", response_model=RequirementAnalysis)
async def analyze_requirements_batch(
    requirement_ids: List[int],
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Analyze multiple requirements using AI"""
    analysis = await requirement_service.analyze_requirements_batch(db, requirement_ids, current_user.id)
    return analysis

@router.post("/{requirement_id}/generate-tasks")
async def generate_tasks_from_requirement(
    requirement_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate tasks from requirement using AI"""
    tasks = await requirement_service.generate_tasks_from_requirement(db, requirement_id, current_user.id)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found or task generation failed"
        )
    return {"message": "Tasks generated successfully", "tasks": tasks}

@router.put("/{requirement_id}/status")
async def update_requirement_status(
    requirement_id: int,
    status_data: RequirementStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update requirement status"""
    requirement = await requirement_service.update_requirement_status(
        db, requirement_id, status_data.status, current_user.id
    )
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return {"message": "Requirement status updated successfully", "status": requirement.status}

@router.get("/{requirement_id}/history", response_model=List[RequirementHistory])
async def get_requirement_history(
    requirement_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get requirement change history"""
    history = await requirement_service.get_requirement_history(db, requirement_id, current_user.id)
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return history

@router.post("/{requirement_id}/approve")
async def approve_requirement(
    requirement_id: int,
    approval_data: RequirementApproval,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Approve requirement"""
    success = await requirement_service.approve_requirement(
        db, requirement_id, approval_data, current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return {"message": "Requirement approved successfully"}

@router.post("/{requirement_id}/reject")
async def reject_requirement(
    requirement_id: int,
    approval_data: RequirementApproval,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Reject requirement"""
    success = await requirement_service.reject_requirement(
        db, requirement_id, approval_data, current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return {"message": "Requirement rejected successfully"}
