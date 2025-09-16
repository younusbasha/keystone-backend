"""
Project Model
"""
from sqlalchemy import Column, String, Text, Enum, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.schemas.project import ProjectStatus, ProjectPriority

class Project(BaseModel):
    """Project model"""
    __tablename__ = 'projects'

    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False)
    priority = Column(Enum(ProjectPriority), default=ProjectPriority.MEDIUM, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget = Column(Float, nullable=True)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="projects")
    requirements = relationship("Requirement", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="project", cascade="all, delete-orphan")
    deployments = relationship("Deployment", back_populates="project", cascade="all, delete-orphan")
