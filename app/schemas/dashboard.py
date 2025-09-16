"""
Dashboard and Analytics Schemas
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class DashboardOverview(BaseModel):
    """Dashboard overview schema"""
    total_projects: int = 0
    active_projects: int = 0
    total_tasks: int = 0
    completed_tasks: int = 0
    total_requirements: int = 0
    active_agents: int = 0

class DashboardStats(BaseModel):
    """Dashboard statistics schema"""
    projects: Dict[str, int] = {}
    tasks: Dict[str, int] = {}
    requirements: Dict[str, int] = {}
    recent_activity_count: int = 0

class DashboardMetrics(BaseModel):
    """Dashboard metrics schema"""
    period: str = "7d"
    metrics: Dict[str, Any] = {}
    trends: Dict[str, List[float]] = {}

class DashboardActivity(BaseModel):
    """Dashboard activity schema"""
    id: int
    action: str
    resource_type: str
    resource_id: int
    user_id: int
    timestamp: datetime
    details: Optional[Dict[str, Any]] = {}

class ActivityFeed(BaseModel):
    """Activity feed schema"""
    activities: List[DashboardActivity]
    total: int
    has_more: bool

class NotificationResponse(BaseModel):
    """Notification response schema"""
    id: int
    title: str
    message: str
    type: str = "info"
    read: bool = False
    created_at: datetime
    user_id: int

class WidgetResponse(BaseModel):
    """Widget response schema"""
    id: int
    name: str
    type: str
    config: Dict[str, Any] = {}
    position: Dict[str, int] = {}
    user_id: int

class WidgetCreate(BaseModel):
    """Widget create schema"""
    name: str
    type: str
    config: Optional[Dict[str, Any]] = {}
    position: Optional[Dict[str, int]] = {}

class WidgetUpdate(BaseModel):
    """Widget update schema"""
    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    position: Optional[Dict[str, int]] = None
