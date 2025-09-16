"""
Project Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    """Project status enumeration"""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ProjectPriority(str, Enum):
    """Project priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ProjectBase(BaseModel):
    """Base project schema"""
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: ProjectPriority = ProjectPriority.MEDIUM
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('Project name must be at least 3 characters long')
        if len(v) > 200:
            raise ValueError('Project name must be at most 200 characters long')
        return v

class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    pass

class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    """Schema for project list response"""
    projects: List[ProjectResponse]
    total: int
    skip: int
    limit: int

class ProjectStats(BaseModel):
    """Project statistics schema"""
    total_requirements: int = 0
    completed_requirements: int = 0
    total_tasks: int = 0
    completed_tasks: int = 0
    team_members: int = 0
    progress_percentage: float = 0.0

class ProjectTeamMember(BaseModel):
    """Project team member schema"""
    user_id: int
    role: str = "member"

class ProjectTeamResponse(BaseModel):
    """Project team response schema"""
    members: List[Dict[str, Any]] = []
    total: int = 0

class ProjectStatusUpdate(BaseModel):
    """Project status update schema"""
    status: ProjectStatus
    comment: Optional[str] = None

class ProjectTimelineResponse(BaseModel):
    """Project timeline response schema"""
    events: List[Dict[str, Any]] = []
    milestones: List[Dict[str, Any]] = []
