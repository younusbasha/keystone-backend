"""
Requirement Model
"""
from sqlalchemy import Column, String, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.schemas.requirement import RequirementType, RequirementPriority, RequirementStatus

class Requirement(BaseModel):
    """Requirement model"""
    __tablename__ = 'requirements'

    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    type = Column(Enum(RequirementType), default=RequirementType.FUNCTIONAL, nullable=False)
    priority = Column(Enum(RequirementPriority), default=RequirementPriority.MEDIUM, nullable=False)
    status = Column(Enum(RequirementStatus), default=RequirementStatus.DRAFT, nullable=False)
    acceptance_criteria = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    ai_analysis = Column(JSON, nullable=True)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)
    created_by = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="requirements")
    creator = relationship("User", back_populates="created_requirements")
    tasks = relationship("Task", back_populates="requirement", cascade="all, delete-orphan")
