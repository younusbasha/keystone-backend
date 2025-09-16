"""
AI Agents Management Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.agent import (
    AgentCreate, AgentUpdate, AgentResponse, AgentExecution,
    AgentAction, AgentActionResponse, AgentAnalytics, AgentMetrics,
    AgentConfiguration, AgentTemplate
)
from app.services.agent_service import agent_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[AgentResponse])
async def get_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all agents"""
    agents = await agent_service.get_agents(db, current_user.id, skip, limit)
    return agents

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new AI agent"""
    agent = await agent_service.create_agent(db, agent_data, current_user.id)
    return AgentResponse.from_orm(agent)

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agent by ID"""
    agent = await agent_service.get_agent_by_id(db, agent_id, current_user.id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return AgentResponse.from_orm(agent)

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update agent"""
    agent = await agent_service.update_agent(db, agent_id, agent_data, current_user.id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return AgentResponse.from_orm(agent)

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete agent"""
    success = await agent_service.delete_agent(db, agent_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return {"message": "Agent deleted successfully"}

@router.post("/{agent_id}/execute")
async def execute_agent(
    agent_id: int,
    execution_data: AgentExecution,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Execute agent with parameters"""
    result = await agent_service.execute_agent(db, agent_id, execution_data, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or execution failed"
        )
    return {"message": "Agent execution started", "execution_id": result.get("execution_id")}

@router.post("/{agent_id}/start")
async def start_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Start agent"""
    success = await agent_service.start_agent(db, agent_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or cannot be started"
        )
    return {"message": "Agent started successfully"}

@router.post("/{agent_id}/stop")
async def stop_agent(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Stop agent"""
    success = await agent_service.stop_agent(db, agent_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or cannot be stopped"
        )
    return {"message": "Agent stopped successfully"}

# Agent Actions

@router.get("/{agent_id}/actions", response_model=List[AgentActionResponse])
async def get_agent_actions(
    agent_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agent actions"""
    actions = await agent_service.get_agent_actions(db, agent_id, current_user.id, skip, limit)
    if actions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return actions

@router.post("/{agent_id}/actions", response_model=AgentActionResponse)
async def create_agent_action(
    agent_id: int,
    action_data: AgentAction,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create agent action"""
    action = await agent_service.create_agent_action(db, agent_id, action_data, current_user.id)
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return AgentActionResponse.from_orm(action)

@router.get("/actions/{action_id}", response_model=AgentActionResponse)
async def get_agent_action(
    action_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agent action by ID"""
    action = await agent_service.get_agent_action_by_id(db, action_id, current_user.id)
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )
    return AgentActionResponse.from_orm(action)

@router.put("/actions/{action_id}", response_model=AgentActionResponse)
async def update_agent_action(
    action_id: int,
    action_data: AgentAction,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update agent action"""
    action = await agent_service.update_agent_action(db, action_id, action_data, current_user.id)
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )
    return AgentActionResponse.from_orm(action)

@router.post("/actions/{action_id}/approve")
async def approve_agent_action(
    action_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Approve agent action"""
    success = await agent_service.approve_agent_action(db, action_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )
    return {"message": "Agent action approved successfully"}

@router.post("/actions/{action_id}/reject")
async def reject_agent_action(
    action_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Reject agent action"""
    success = await agent_service.reject_agent_action(db, action_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )
    return {"message": "Agent action rejected successfully"}

@router.post("/actions/{action_id}/retry")
async def retry_agent_action(
    action_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Retry agent action"""
    success = await agent_service.retry_agent_action(db, action_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found or cannot be retried"
        )
    return {"message": "Agent action retry initiated successfully"}

# Agent Analytics

@router.get("/analytics/overview", response_model=AgentAnalytics)
async def get_agents_analytics_overview(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agents analytics overview"""
    analytics = await agent_service.get_agents_analytics_overview(db, current_user.id)
    return analytics

@router.get("/analytics/performance", response_model=AgentAnalytics)
async def get_agents_performance_analytics(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agents performance analytics"""
    analytics = await agent_service.get_agents_performance_analytics(db, current_user.id)
    return analytics

@router.get("/{agent_id}/logs")
async def get_agent_logs(
    agent_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agent logs"""
    logs = await agent_service.get_agent_logs(db, agent_id, current_user.id, skip, limit)
    if logs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return {"logs": logs}

@router.get("/{agent_id}/metrics", response_model=AgentMetrics)
async def get_agent_metrics(
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agent metrics"""
    metrics = await agent_service.get_agent_metrics(db, agent_id, current_user.id)
    if not metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return metrics

@router.post("/{agent_id}/configure")
async def configure_agent(
    agent_id: int,
    config_data: AgentConfiguration,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Configure agent settings"""
    success = await agent_service.configure_agent(db, agent_id, config_data, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return {"message": "Agent configured successfully"}

@router.get("/templates", response_model=List[AgentTemplate])
async def get_agent_templates(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get agent templates"""
    templates = await agent_service.get_agent_templates(db, current_user.id)
    return templates
