"""
Task Management Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enumeration"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class TaskPriority(str, Enum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskCreate(BaseModel):
    """Schema for creating a task"""
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    requirement_id: Optional[int] = None
    assigned_to: Optional[int] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    """Schema for task response"""
    id: int
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    requirement_id: Optional[int] = None
    assigned_to: Optional[int] = None
    priority: TaskPriority
    status: TaskStatus
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskStatusUpdate(BaseModel):
    """Schema for task status update"""
    status: TaskStatus
    comment: Optional[str] = None

class TaskComment(BaseModel):
    """Schema for task comment"""
    content: str

class TaskCommentResponse(BaseModel):
    """Schema for task comment response"""
    id: int
    task_id: int
    content: str
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskAssignment(BaseModel):
    """Schema for task assignment"""
    user_id: int
    comment: Optional[str] = None

class TaskTimeLog(BaseModel):
    """Schema for task time log"""
    hours: float
    description: Optional[str] = None
    date: Optional[datetime] = None

class TaskTimeLogResponse(BaseModel):
    """Schema for task time log response"""
    id: int
    task_id: int
    user_id: int
    hours: float
    description: Optional[str] = None
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class TaskAttachment(BaseModel):
    """Schema for task attachment"""
    id: int
    task_id: int
    filename: str
    file_path: str
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskDependencyCreate(BaseModel):
    """Schema for creating task dependency"""
    dependent_task_id: int
    dependency_type: str = "blocks"  # blocks, depends_on, etc.

class TaskCommentCreate(BaseModel):
    """Schema for creating task comment"""
    content: str
    parent_id: Optional[int] = None  # For threaded comments
