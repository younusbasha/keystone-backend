"""
User Model
"""
from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.permission import user_roles

class User(BaseModel):
    """User model"""
    __tablename__ = 'users'

    # BaseModel now provides UUID id, created_at, updated_at, is_deleted
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)

    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    created_requirements = relationship("Requirement", back_populates="creator", cascade="all, delete-orphan")
    created_integrations = relationship("Integration", back_populates="creator", cascade="all, delete-orphan")

    # Task relationships
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    created_tasks = relationship("Task", foreign_keys="Task.created_by", back_populates="creator")

    # Many-to-many relationship with roles
    roles = relationship(
        "Role",
        secondary=user_roles,
        primaryjoin="User.id == user_roles.c.user_id",
        secondaryjoin="Role.id == user_roles.c.role_id",
        back_populates="users"
    )
