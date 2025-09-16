"""
Permissions & Roles Management Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.permission import (
    PermissionResponse, UserPermissionUpdate, RoleCreate,
    RoleUpdate, RoleResponse, ProjectPermissionUpdate
)
from app.services.permission_service import permission_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

# Permissions Management

@router.get("/", response_model=List[PermissionResponse])
async def get_permissions(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all available permissions"""
    permissions = await permission_service.get_all_permissions(db, current_user.id)
    return permissions

@router.get("/user/{user_id}", response_model=List[PermissionResponse])
async def get_user_permissions(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user permissions"""
    permissions = await permission_service.get_user_permissions(db, user_id, current_user.id)
    if permissions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return permissions

@router.put("/user/{user_id}")
async def update_user_permissions(
    user_id: int,
    permission_data: UserPermissionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user permissions (admin only)"""
    success = await permission_service.update_user_permissions(db, user_id, permission_data, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User permissions updated successfully"}

@router.get("/project/{project_id}", response_model=List[PermissionResponse])
async def get_project_permissions(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get project permissions"""
    permissions = await permission_service.get_project_permissions(db, project_id, current_user.id)
    if permissions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return permissions

@router.put("/project/{project_id}")
async def update_project_permissions(
    project_id: int,
    permission_data: ProjectPermissionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update project permissions"""
    success = await permission_service.update_project_permissions(db, project_id, permission_data, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return {"message": "Project permissions updated successfully"}

# Roles Management

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all roles"""
    roles = await permission_service.get_all_roles(db, current_user.id)
    return roles

@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new role (admin only)"""
    role = await permission_service.create_role(db, role_data, current_user.id)
    return RoleResponse.from_orm(role)

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update role (admin only)"""
    role = await permission_service.update_role(db, role_id, role_data, current_user.id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return RoleResponse.from_orm(role)

@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete role (admin only)"""
    success = await permission_service.delete_role(db, role_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return {"message": "Role deleted successfully"}
