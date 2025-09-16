"""
Integration and Deployment Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum

class IntegrationType(str, Enum):
    """Integration type enumeration"""
    GITHUB = "github"
    GITLAB = "gitlab"
    JIRA = "jira"
    SLACK = "slack"
    JENKINS = "jenkins"
    DOCKER = "docker"
    AWS = "aws"
    AZURE = "azure"

class IntegrationStatus(str, Enum):
    """Integration status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    TESTING = "testing"

class IntegrationCreate(BaseModel):
    """Schema for creating an integration"""
    name: str
    type: IntegrationType
    config: Dict[str, Any] = {}
    description: Optional[str] = None

class IntegrationUpdate(BaseModel):
    """Schema for updating an integration"""
    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class IntegrationResponse(BaseModel):
    """Schema for integration response"""
    id: int
    name: str
    type: IntegrationType
    status: IntegrationStatus = IntegrationStatus.INACTIVE
    config: Dict[str, Any] = {}
    description: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DeploymentCreate(BaseModel):
    """Schema for creating a deployment"""
    project_id: int
    environment: str
    version: str
    config: Optional[Dict[str, Any]] = {}

class DeploymentUpdate(BaseModel):
    """Schema for updating a deployment"""
    version: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class DeploymentResponse(BaseModel):
    """Schema for deployment response"""
    id: int
    project_id: int
    environment: str
    version: str
    status: str = "pending"
    config: Dict[str, Any] = {}
    deployed_by: int
    deployed_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WebhookData(BaseModel):
    """Schema for webhook data"""
    event_type: str
    payload: Dict[str, Any]
    headers: Optional[Dict[str, str]] = None

class IntegrationType(BaseModel):
    """Schema for integration type"""
    type: str
    name: str
    description: str
    required_config: List[str] = []
    optional_config: List[str] = []
