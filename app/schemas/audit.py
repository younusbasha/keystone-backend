"""
Audit and Logging Schemas
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class AuditLogResponse(BaseModel):
    """Audit log response schema"""
    id: int
    action: str
    resource_type: str
    resource_id: Optional[int] = None
    user_id: int
    timestamp: datetime
    details: Optional[Dict[str, Any]] = {}
    ip_address: Optional[str] = None

class UserActivityResponse(BaseModel):
    """User activity response schema"""
    id: int
    user_id: int
    action: str
    resource_type: str
    resource_id: Optional[int] = None
    timestamp: datetime
    details: Optional[Dict[str, Any]] = {}

class SystemEventResponse(BaseModel):
    """System event response schema"""
    id: int
    event_type: str
    severity: str = "info"
    message: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = {}
