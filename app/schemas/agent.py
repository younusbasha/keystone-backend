"""
AI Agent Management Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
    """Agent type enumeration"""
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    ANALYSIS = "analysis"

class AgentStatus(str, Enum):
    """Agent status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class AgentCreate(BaseModel):
    """Schema for creating an agent"""
    name: str
    description: str
    type: AgentType
    config: Optional[Dict[str, Any]] = {}

class AgentUpdate(BaseModel):
    """Schema for updating an agent"""
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    """Schema for agent response"""
    id: int
    name: str
    description: str
    type: AgentType
    status: AgentStatus = AgentStatus.INACTIVE
    config: Dict[str, Any] = {}
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgentExecution(BaseModel):
    """Schema for agent execution"""
    parameters: Dict[str, Any] = {}
    priority: str = "normal"

class AgentAction(BaseModel):
    """Schema for agent action"""
    action_type: str
    parameters: Dict[str, Any] = {}
    description: Optional[str] = None

class AgentActionResponse(BaseModel):
    """Schema for agent action response"""
    id: int
    agent_id: int
    action_type: str
    parameters: Dict[str, Any] = {}
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AgentAnalytics(BaseModel):
    """Schema for agent analytics"""
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_execution_time: float = 0.0
    metrics: Dict[str, Any] = {}

class AgentMetrics(BaseModel):
    """Schema for agent metrics"""
    agent_id: int
    uptime: float = 0.0
    success_rate: float = 0.0
    avg_response_time: float = 0.0
    total_actions: int = 0

class AgentConfiguration(BaseModel):
    """Schema for agent configuration"""
    config: Dict[str, Any]
    enabled: bool = True

class AgentTemplate(BaseModel):
    """Schema for agent template"""
    id: int
    name: str
    type: AgentType
    description: str
    default_config: Dict[str, Any] = {}
    parameters: List[Dict[str, Any]] = []
