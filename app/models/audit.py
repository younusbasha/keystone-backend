"""
Audit and Logging Models
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
import uuid

from app.models.base import BaseModel


class ActionType(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    APPROVE = "approve"
    REJECT = "reject"
    DEPLOY = "deploy"
    ROLLBACK = "rollback"


class EntityType(str, Enum):
    USER = "user"
    PROJECT = "project"
    REQUIREMENT = "requirement"
    TASK = "task"
    AGENT = "agent"
    DEPLOYMENT = "deployment"
    INTEGRATION = "integration"


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditLog(BaseModel):
    """Comprehensive audit logging for compliance and security"""
    __tablename__ = "audit_logs"

    # Who performed the action
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    agent_id = Column(String(36), ForeignKey("ai_agents.id"), nullable=True)
    session_id = Column(String(255), nullable=True)

    # What action was performed
    action_type = Column(String(20), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(36), nullable=True)
    description = Column(Text, nullable=False)

    # Data changes
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    additional_data = Column(JSON, nullable=True)

    # Request context
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    endpoint = Column(String(255), nullable=True)
    request_id = Column(String(255), nullable=True)

    # Security and compliance
    risk_score = Column(Integer, default=0)
    security_flags = Column(JSON, nullable=True)
    compliance_category = Column(String(50), nullable=True)
    retention_period_days = Column(Integer, default=2555)  # 7 years default

    # Relationships
    user = relationship("User")
    agent = relationship("AIAgent")


class SystemLog(BaseModel):
    """System-level logging for debugging and monitoring"""
    __tablename__ = "system_logs"

    level = Column(String(10), nullable=False)
    message = Column(Text, nullable=False)
    component = Column(String(100), nullable=False)

    # Context
    context = Column(JSON, nullable=True)
    stack_trace = Column(Text, nullable=True)
    request_id = Column(String(255), nullable=True)

    # Performance metrics
    execution_time = Column(Integer, nullable=True)  # milliseconds
    memory_usage = Column(Integer, nullable=True)  # bytes
    cpu_usage = Column(Integer, nullable=True)  # percentage


class SecurityEvent(BaseModel):
    """Security-related events and incidents"""
    __tablename__ = "security_events"

    event_type = Column(String(50), nullable=False)
    severity = Column(String(10), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)

    # Event context
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)

    # Investigation
    investigated = Column(Boolean, default=False)
    resolved = Column(Boolean, default=False)
    investigated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    investigator = relationship("User", foreign_keys=[investigated_by])
