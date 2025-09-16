"""
Permission and Role Management Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class PermissionResponse(BaseModel):
    """Permission response schema"""
    id: int
    name: str
    description: str
    resource: str
    action: str

class RoleResponse(BaseModel):
    """Role response schema"""
    id: int
    name: str
    description: str
    permissions: List[PermissionResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    """Role create schema"""
    name: str
    description: str
    permissions: List[str] = []

class RoleUpdate(BaseModel):
    """Role update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None

class UserPermissions(BaseModel):
    """User permissions schema"""
    user_id: int
    roles: List[RoleResponse] = []
    direct_permissions: List[PermissionResponse] = []

class ProjectPermissions(BaseModel):
    """Project permissions schema"""
    project_id: int
    members: List[Dict[str, Any]] = []
    roles: List[RoleResponse] = []
