"""
Requirement Management Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum

class RequirementType(str, Enum):
    """Requirement type enumeration"""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    USER_STORY = "user_story"

class RequirementStatus(str, Enum):
    """Requirement status enumeration"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"

class RequirementPriority(str, Enum):
    """Requirement priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RequirementCreate(BaseModel):
    """Schema for creating a requirement"""
    title: str
    description: str
    project_id: int
    priority: RequirementPriority = RequirementPriority.MEDIUM
    status: RequirementStatus = RequirementStatus.DRAFT
    acceptance_criteria: Optional[str] = None

class RequirementUpdate(BaseModel):
    """Schema for updating a requirement"""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[RequirementPriority] = None
    status: Optional[RequirementStatus] = None
    acceptance_criteria: Optional[str] = None

class RequirementResponse(BaseModel):
    """Schema for requirement response"""
    id: int
    title: str
    description: str
    project_id: int
    priority: RequirementPriority
    status: RequirementStatus
    acceptance_criteria: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RequirementListResponse(BaseModel):
    """Schema for requirement list response"""
    requirements: List[RequirementResponse]
    total: int
    skip: int
    limit: int

class RequirementAnalysis(BaseModel):
    """Schema for requirement AI analysis"""
    requirement_id: int
    complexity_score: float = 0.0
    estimated_effort: int = 0
    suggested_tasks: List[Dict[str, Any]] = []
    analysis_summary: str = ""
    recommendations: List[str] = []

class RequirementAnalysisResponse(BaseModel):
    """Schema for requirement AI analysis response"""
    requirement_id: int
    complexity_score: float = 0.0
    estimated_effort: int = 0
    suggested_tasks: List[Dict[str, Any]] = []
    analysis_summary: str = ""
    recommendations: List[str] = []
    analyzed_at: datetime

class RequirementStatusUpdate(BaseModel):
    """Schema for requirement status update"""
    status: RequirementStatus
    comment: Optional[str] = None

class RequirementHistory(BaseModel):
    """Schema for requirement history"""
    id: int
    requirement_id: int
    action: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    changed_by: int
    timestamp: datetime

class RequirementApproval(BaseModel):
    """Schema for requirement approval/rejection"""
    comment: Optional[str] = None
