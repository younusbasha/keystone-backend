"""
Audit & Logging Endpoints
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.audit import (
    AuditLogResponse, UserActivityResponse,
    SystemEventResponse, SecurityEventResponse
)
from app.services.audit_service import audit_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    entity_type: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get audit logs with filters"""
    logs = await audit_service.get_audit_logs(
        db, current_user.id, skip, limit, entity_type, action, user_id, start_date, end_date
    )
    return logs

@router.get("/logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get audit log by ID"""
    log = await audit_service.get_audit_log_by_id(db, log_id, current_user.id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found"
        )
    return AuditLogResponse.from_orm(log)

@router.get("/user-activity", response_model=List[UserActivityResponse])
async def get_user_activity(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = Query(None),
    activity_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user activity logs"""
    activity = await audit_service.get_user_activity(
        db, current_user.id, skip, limit, user_id, activity_type, start_date, end_date
    )
    return activity

@router.get("/system-events", response_model=List[SystemEventResponse])
async def get_system_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system events"""
    events = await audit_service.get_system_events(
        db, current_user.id, skip, limit, event_type, severity, start_date, end_date
    )
    return events

@router.get("/security-events", response_model=List[SecurityEventResponse])
async def get_security_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_type: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get security events"""
    events = await audit_service.get_security_events(
        db, current_user.id, skip, limit, event_type, risk_level, start_date, end_date
    )
    return events
