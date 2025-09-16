"""
AI Agent Models
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.orm import relationship
import uuid

from app.models.base import BaseModel


class AgentType(str, Enum):
    CODEGEN = "codegen"
    TEST = "test"
    REVIEW = "review"
    TASK_PLANNER = "task_planner"
    INTEGRATION = "integration"
    QA = "qa"
    DEPLOYMENT = "deployment"
    ANALYSIS = "analysis"


class AgentStatus(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class ActionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_REVIEW = "requires_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AIAgent(BaseModel):
    """AI Agent model for autonomous task execution"""
    __tablename__ = "ai_agents"

    name = Column(String(255), nullable=False)
    agent_type = Column(String(20), nullable=False)
    status = Column(String(20), default=AgentStatus.IDLE)
    version = Column(String(50), default="1.0.0")

    # Configuration
    capabilities = Column(JSON, nullable=True)  # List of agent capabilities
    configuration = Column(JSON, nullable=True)  # Agent-specific config
    permissions = Column(JSON, nullable=True)  # What the agent can access/modify

    # Performance metrics
    success_rate = Column(Float, default=0.0)
    average_confidence = Column(Float, default=0.0)
    total_actions = Column(Integer, default=0)
    successful_actions = Column(Integer, default=0)

    # Resource limits
    max_concurrent_actions = Column(Integer, default=5)
    current_load = Column(Integer, default=0)

    # Relationships
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    actions = relationship("AgentAction", back_populates="agent")
    decisions = relationship("AgentDecision", back_populates="agent")


class AgentAction(BaseModel):
    """Records of AI Agent actions"""
    __tablename__ = "agent_actions"

    agent_id = Column(String(36), ForeignKey("ai_agents.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # code_generation, test_creation, review, etc.
    status = Column(String(20), default=ActionStatus.PENDING)

    # Action context
    target_type = Column(String(50), nullable=True)  # task, requirement, project
    target_id = Column(String(36), nullable=True)

    # Action details
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)

    # AI metrics
    confidence_score = Column(Float, nullable=True)
    risk_level = Column(String(20), default=RiskLevel.LOW)

    # Execution timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)

    # Review process
    requires_human_review = Column(Boolean, default=False)
    reviewed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    review_comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    agent = relationship("AIAgent", back_populates="actions")
    reviewer = relationship("User")


class AgentDecision(BaseModel):
    """AI Agent decision records for audit and learning"""
    __tablename__ = "agent_decisions"

    agent_id = Column(String(36), ForeignKey("ai_agents.id"), nullable=False)
    decision_type = Column(String(50), nullable=False)
    context = Column(JSON, nullable=True)
    decision_data = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    outcome = Column(String(20), nullable=True)  # success, failure, pending

    # Relationships
    agent = relationship("AIAgent", back_populates="decisions")


class AgentWorkflow(BaseModel):
    """Workflow templates for AI agents"""
    __tablename__ = "agent_workflows"

    name = Column(String(255), nullable=False)
    agent_type = Column(String(20), nullable=False)
    workflow_steps = Column(JSON, nullable=False)
    trigger_conditions = Column(JSON, nullable=True)
    success_criteria = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
