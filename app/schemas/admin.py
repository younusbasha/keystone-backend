"""
Admin System Schemas
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from datetime import datetime

class SystemSettings(BaseModel):
    """System settings schema"""
    maintenance_mode: bool = False
    registration_enabled: bool = True
    max_users: Optional[int] = None
    session_timeout: int = 3600
    settings: Dict[str, Any] = {}

class SystemHealth(BaseModel):
    """System health schema"""
    status: str = "healthy"
    database: str = "connected"
    cache: str = "connected"
    services: Dict[str, str] = {}
    uptime: int = 0
    timestamp: datetime

class SystemStatus(BaseModel):
    """System status schema"""
    version: str
    environment: str = "development"
    database_status: str = "connected"
    active_users: int = 0
    total_projects: int = 0
    total_tasks: int = 0
    system_load: Dict[str, float] = {}

class BackupResponse(BaseModel):
    """Backup response schema"""
    backup_id: str
    backup_type: str
    status: str = "created"
    file_path: str
    size_bytes: int = 0
    created_at: datetime

class RestoreRequest(BaseModel):
    """Restore request schema"""
    backup_id: str
    restore_type: str = "full"
    options: Dict[str, Any] = {}
