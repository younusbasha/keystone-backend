"""
System Administration Endpoints
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.admin import (
    SystemSettings, SystemHealth, SystemStatus,
    BackupResponse, RestoreRequest
)
from app.services.admin_service import admin_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/settings", response_model=SystemSettings)
async def get_system_settings(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system settings (admin only)"""
    settings = await admin_service.get_system_settings(db, current_user.id)
    return settings

@router.put("/settings", response_model=SystemSettings)
async def update_system_settings(
    settings_data: SystemSettings,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update system settings (admin only)"""
    settings = await admin_service.update_system_settings(db, settings_data, current_user.id)
    return settings

@router.get("/health", response_model=SystemHealth)
async def get_system_health(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system health status"""
    health = await admin_service.get_system_health(db, current_user.id)
    return health

@router.get("/version")
async def get_system_version(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system version information"""
    version = await admin_service.get_system_version(db, current_user.id)
    return {"version": version}

@router.get("/system-status", response_model=SystemStatus)
async def get_system_status(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive system status"""
    status_info = await admin_service.get_system_status(db, current_user.id)
    return status_info

@router.post("/backup", response_model=BackupResponse)
async def create_system_backup(
    backup_type: str = Query("full", description="Backup type: full, incremental, or differential"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create system backup (admin only)"""
    backup = await admin_service.create_system_backup(db, backup_type, current_user.id)
    if not backup:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Backup creation failed"
        )
    return backup

@router.post("/restore")
async def restore_system(
    restore_data: RestoreRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Restore system from backup (admin only)"""
    success = await admin_service.restore_system(db, restore_data, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="System restore failed"
        )
    return {"message": "System restore initiated successfully"}

@router.get("/logs")
async def get_system_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    level: Optional[str] = Query(None, description="Log level filter"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system logs (admin only)"""
    logs = await admin_service.get_system_logs(
        db, current_user.id, skip, limit, level, start_date, end_date
    )
    return {"logs": logs}
