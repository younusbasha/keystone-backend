"""
Permissions and RBAC Models
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.models.base import BaseModel


# Association tables for many-to-many relationships
user_roles = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('role_id', String(36), ForeignKey('roles.id'), primary_key=True),
    Column('assigned_at', DateTime, default=datetime.utcnow),
    Column('assigned_by', String(36), ForeignKey('users.id'))
)

role_permissions = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('role_id', String(36), ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', String(36), ForeignKey('permissions.id'), primary_key=True),
    Column('granted_at', DateTime, default=datetime.utcnow),
    Column('granted_by', String(36), ForeignKey('users.id'))
)

class ResourceType(str, Enum):
    PROJECT = "project"
    REQUIREMENT = "requirement"
    TASK = "task"
    AGENT = "agent"
    DEPLOYMENT = "deployment"
    INTEGRATION = "integration"
    USER = "user"
    AUDIT_LOG = "audit_log"
    SYSTEM_SETTING = "system_setting"


class PermissionType(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    DEPLOY = "deploy"
    ADMIN = "admin"


class Role(BaseModel):
    """User roles for RBAC"""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Role hierarchy
    parent_role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True)
    level = Column(Integer, default=0)  # 0=highest, higher numbers = lower level

    # Configuration
    is_system_role = Column(Boolean, default=False)  # Built-in roles
    is_active = Column(Boolean, default=True)

    # Relationships
    parent_role = relationship("Role", remote_side=[id], back_populates="child_roles")
    child_roles = relationship("Role", back_populates="parent_role")
    users = relationship(
        "User",
        secondary=user_roles,
        primaryjoin="Role.id == user_roles.c.role_id",
        secondaryjoin="User.id == user_roles.c.user_id",
        back_populates="roles"
    )
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(BaseModel):
    """Granular permissions for resources"""
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Permission details
    resource_type = Column(String(50), nullable=False)
    permission_type = Column(String(20), nullable=False)

    # Scope and conditions
    scope = Column(JSON, nullable=True)  # Additional conditions/filters
    is_system_permission = Column(Boolean, default=False)

    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


class ProjectPermission(BaseModel):
    """Project-specific permissions (project-level RBAC)"""
    __tablename__ = "project_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)

    # Permission scope within project
    permissions = Column(JSON, nullable=True)  # Specific permissions override

    # Validity
    granted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    project = relationship("Project")
    user = relationship("User", foreign_keys=[user_id])
    role = relationship("Role")
    granter = relationship("User", foreign_keys=[granted_by])


class AgentPermission(BaseModel):
    """AI Agent permissions and capabilities"""
    __tablename__ = "agent_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("ai_agents.id"), nullable=False)

    # Resource access
    resource_type = Column(String(50), nullable=False)
    allowed_actions = Column(JSON, nullable=False)  # List of allowed actions

    # Constraints
    max_risk_level = Column(String(10), default="medium")  # Maximum risk level agent can handle
    requires_approval_above = Column(String(10), default="high")  # Risk level requiring approval

    # Scope limitations
    project_scope = Column(JSON, nullable=True)  # Which projects agent can access
    resource_filters = Column(JSON, nullable=True)  # Additional filters

    # Time-based restrictions
    valid_from = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("AIAgent")


class SystemSetting(BaseModel):
    """System-wide configuration settings"""
    __tablename__ = "system_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(100), nullable=False)  # security, ai, integration, etc.
    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=False)

    last_modified_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    description = Column(Text, nullable=True)
    data_type = Column(String(50), nullable=False)  # string, int, bool, json, etc.
    is_sensitive = Column(Boolean, default=False)  # Encrypt sensitive values

    # Validation
    validation_rules = Column(JSON, nullable=True)  # JSON schema for validation

    # Access control
    requires_permission = Column(String(100), nullable=True)
    last_modified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Make key unique within category
    __table_args__ = (UniqueConstraint('category', 'key', name='uix_category_key'),)

    # Relationships
    modifier = relationship("User")
