"""
Task Models
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.orm import relationship
import uuid

from app.models.base import BaseModel


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    REVIEW = "review"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"
    BUG_FIX = "bug_fix"


class Task(BaseModel):
    """Task model for development tasks"""
    __tablename__ = "tasks"

    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20), default=TaskStatus.PENDING)
    priority = Column(String(20), default=TaskPriority.MEDIUM)
    task_type = Column(String(20), default=TaskType.DEVELOPMENT)

    # Relationships
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    requirement_id = Column(String(36), ForeignKey("requirements.id"), nullable=True)
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)

    # Task metrics
    estimated_hours = Column(Float, nullable=True)
    actual_hours = Column(Float, nullable=True)
    complexity_score = Column(Float, default=1.0)  # 1-10 scale
    ai_confidence = Column(Float, nullable=True)  # AI confidence in task breakdown

    # Dates
    due_date = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # AI Generated fields
    ai_generated = Column(Boolean, default=False)
    ai_suggestions = Column(JSON, nullable=True)
    acceptance_criteria = Column(JSON, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="tasks")
    requirement = relationship("Requirement", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_tasks")
    dependencies = relationship("TaskDependency", foreign_keys="TaskDependency.task_id", back_populates="task")
    dependent_tasks = relationship("TaskDependency", foreign_keys="TaskDependency.depends_on_id", back_populates="depends_on")
    comments = relationship("TaskComment", back_populates="task")


class TaskDependency(BaseModel):
    """Task dependency relationships"""
    __tablename__ = "task_dependencies"

    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False)
    depends_on_id = Column(String(36), ForeignKey("tasks.id"), nullable=False)
    dependency_type = Column(String(20), default="blocks")  # blocks, depends_on

    # Relationships
    task = relationship("Task", foreign_keys=[task_id], back_populates="dependencies")
    depends_on = relationship("Task", foreign_keys=[depends_on_id], back_populates="dependent_tasks")


class TaskComment(BaseModel):
    """Comments on tasks"""
    __tablename__ = "task_comments"

    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    comment_type = Column(String(20), default="general")  # general, review, question

    # Relationships
    task = relationship("Task", back_populates="comments")
    user = relationship("User")
