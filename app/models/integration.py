"""
Integration Models for external services
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
import uuid

from app.models.base import BaseModel


class IntegrationType(str, Enum):
    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"
    JIRA = "jira"
    ASANA = "asana"
    TRELLO = "trello"
    JENKINS = "jenkins"
    GITHUB_ACTIONS = "github_actions"
    AZURE_DEVOPS = "azure_devops"
    GCP = "gcp"
    AWS = "aws"
    AZURE = "azure"
    SLACK = "slack"
    TEAMS = "teams"
    FIREBASE = "firebase"


class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"
    EXPIRED = "expired"


class DeploymentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class Integration(BaseModel):
    """External service integrations"""
    __tablename__ = "integrations"

    name = Column(String(255), nullable=False)
    integration_type = Column(String(50), nullable=False)
    status = Column(String(20), default=IntegrationStatus.PENDING)

    # Connection details
    endpoint_url = Column(String(500), nullable=True)
    api_version = Column(String(20), nullable=True)

    # Authentication (encrypted)
    auth_type = Column(String(50), nullable=False)  # oauth, api_key, token, etc.
    credentials = Column(JSON, nullable=True)  # Encrypted credentials

    # Configuration
    config = Column(JSON, nullable=True)
    webhook_secret = Column(String(255), nullable=True)

    # Health monitoring
    last_health_check = Column(DateTime, nullable=True)
    health_status = Column(String(20), nullable=True)
    error_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)

    # Project association
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="integrations")
    creator = relationship("User", back_populates="created_integrations")
    events = relationship("IntegrationEvent", back_populates="integration")


class IntegrationEvent(BaseModel):
    """Events and webhooks from integrated services"""
    __tablename__ = "integration_events"

    integration_id = Column(String(36), ForeignKey("integrations.id"), nullable=False)

    event_type = Column(String(100), nullable=False)  # push, pull_request, issue_created, etc.
    event_source = Column(String(50), nullable=False)  # webhook, polling, manual

    # Event data
    raw_payload = Column(JSON, nullable=True)
    processed_data = Column(JSON, nullable=True)

    # Processing status
    processed = Column(Boolean, default=False)
    processing_error = Column(Text, nullable=True)

    # Relationships
    integration = relationship("Integration", back_populates="events")


class Deployment(BaseModel):
    """Deployment tracking and management"""
    __tablename__ = "deployments"

    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    version = Column(String(50), nullable=False)
    environment = Column(String(50), nullable=False)  # development, staging, production
    status = Column(String(20), default=DeploymentStatus.PENDING)

    # Deployment details
    deployment_type = Column(String(30), default="rolling")  # rolling, blue-green, canary
    commit_hash = Column(String(40), nullable=True)
    branch = Column(String(100), nullable=True)
    tag = Column(String(100), nullable=True)

    # Configuration and artifacts
    config = Column(JSON, nullable=True)
    artifacts = Column(JSON, nullable=True)

    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Results
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    rollback_reason = Column(Text, nullable=True)

    # User tracking
    deployed_by = Column(String(36), ForeignKey("users.id"), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="deployments")
    deployer = relationship("User")
    health_checks = relationship("DeploymentHealthCheck", back_populates="deployment")


class DeploymentHealthCheck(BaseModel):
    """Health checks for deployments"""
    __tablename__ = "deployment_health_checks"

    deployment_id = Column(String(36), ForeignKey("deployments.id"), nullable=False)
    check_type = Column(String(50), nullable=False)  # http, tcp, database, custom
    endpoint = Column(String(500), nullable=True)
    expected_status = Column(String(20), nullable=True)
    actual_status = Column(String(20), nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)

    # Relationships
    deployment = relationship("Deployment", back_populates="health_checks")
