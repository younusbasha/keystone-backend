"""
Integrations & Deployments Management Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.integration import (
    IntegrationCreate, IntegrationUpdate, IntegrationResponse,
    IntegrationTest, IntegrationSync, IntegrationLog,
    DeploymentCreate, DeploymentUpdate, DeploymentResponse,
    DeploymentEnvironment
)
from app.services.integration_service import integration_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

# Integrations Management

@router.get("/", response_model=List[IntegrationResponse])
async def get_integrations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all integrations"""
    integrations = await integration_service.get_integrations(db, current_user.id, skip, limit)
    return integrations

@router.post("/", response_model=IntegrationResponse, status_code=status.HTTP_201_CREATED)
async def create_integration(
    integration_data: IntegrationCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new integration"""
    integration = await integration_service.create_integration(db, integration_data, current_user.id)
    return IntegrationResponse.from_orm(integration)

@router.get("/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    integration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get integration by ID"""
    integration = await integration_service.get_integration_by_id(db, integration_id, current_user.id)
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return IntegrationResponse.from_orm(integration)

@router.put("/{integration_id}", response_model=IntegrationResponse)
async def update_integration(
    integration_id: int,
    integration_data: IntegrationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update integration"""
    integration = await integration_service.update_integration(db, integration_id, integration_data, current_user.id)
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return IntegrationResponse.from_orm(integration)

@router.delete("/{integration_id}")
async def delete_integration(
    integration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete integration"""
    success = await integration_service.delete_integration(db, integration_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return {"message": "Integration deleted successfully"}

@router.post("/{integration_id}/test")
async def test_integration(
    integration_id: int,
    test_data: IntegrationTest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Test integration connection"""
    result = await integration_service.test_integration(db, integration_id, test_data, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return {"message": "Integration test completed", "result": result}

@router.post("/{integration_id}/sync")
async def sync_integration(
    integration_id: int,
    sync_data: IntegrationSync,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Sync integration data"""
    result = await integration_service.sync_integration(db, integration_id, sync_data, current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found or sync failed"
        )
    return {"message": "Integration sync initiated", "sync_id": result.get("sync_id")}

@router.get("/{integration_id}/logs", response_model=List[IntegrationLog])
async def get_integration_logs(
    integration_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get integration logs"""
    logs = await integration_service.get_integration_logs(db, integration_id, current_user.id, skip, limit)
    if logs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return logs

@router.put("/{integration_id}/enable")
async def enable_integration(
    integration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Enable integration"""
    success = await integration_service.enable_integration(db, integration_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return {"message": "Integration enabled successfully"}

@router.put("/{integration_id}/disable")
async def disable_integration(
    integration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Disable integration"""
    success = await integration_service.disable_integration(db, integration_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return {"message": "Integration disabled successfully"}

@router.get("/types")
async def get_integration_types(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get available integration types"""
    types = await integration_service.get_integration_types(db, current_user.id)
    return {"types": types}

@router.post("/{integration_id}/webhook")
async def create_integration_webhook(
    integration_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create webhook for integration"""
    webhook = await integration_service.create_integration_webhook(db, integration_id, current_user.id)
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    return {"message": "Webhook created successfully", "webhook": webhook}

# Deployments Management

@router.get("/deployments", response_model=List[DeploymentResponse])
async def get_deployments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all deployments"""
    deployments = await integration_service.get_deployments(db, current_user.id, skip, limit)
    return deployments

@router.post("/deployments", response_model=DeploymentResponse, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    deployment_data: DeploymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new deployment"""
    deployment = await integration_service.create_deployment(db, deployment_data, current_user.id)
    return DeploymentResponse.from_orm(deployment)

@router.get("/deployments/{deployment_id}", response_model=DeploymentResponse)
async def get_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get deployment by ID"""
    deployment = await integration_service.get_deployment_by_id(db, deployment_id, current_user.id)
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    return DeploymentResponse.from_orm(deployment)

@router.put("/deployments/{deployment_id}", response_model=DeploymentResponse)
async def update_deployment(
    deployment_id: int,
    deployment_data: DeploymentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update deployment"""
    deployment = await integration_service.update_deployment(db, deployment_id, deployment_data, current_user.id)
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    return DeploymentResponse.from_orm(deployment)

@router.delete("/deployments/{deployment_id}")
async def delete_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete deployment"""
    success = await integration_service.delete_deployment(db, deployment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    return {"message": "Deployment deleted successfully"}

@router.post("/deployments/{deployment_id}/rollback")
async def rollback_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Rollback deployment"""
    success = await integration_service.rollback_deployment(db, deployment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found or cannot be rolled back"
        )
    return {"message": "Deployment rollback initiated successfully"}

@router.post("/deployments/{deployment_id}/promote")
async def promote_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Promote deployment to next environment"""
    success = await integration_service.promote_deployment(db, deployment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found or cannot be promoted"
        )
    return {"message": "Deployment promotion initiated successfully"}

@router.get("/deployments/{deployment_id}/logs")
async def get_deployment_logs(
    deployment_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get deployment logs"""
    logs = await integration_service.get_deployment_logs(db, deployment_id, current_user.id, skip, limit)
    if logs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    return {"logs": logs}

@router.get("/deployments/{deployment_id}/status")
async def get_deployment_status(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get deployment status"""
    status_info = await integration_service.get_deployment_status(db, deployment_id, current_user.id)
    if not status_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    return {"status": status_info}

@router.post("/deployments/{deployment_id}/restart")
async def restart_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Restart deployment"""
    success = await integration_service.restart_deployment(db, deployment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found or cannot be restarted"
        )
    return {"message": "Deployment restart initiated successfully"}

@router.get("/deployments/environments", response_model=List[DeploymentEnvironment])
async def get_deployment_environments(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get available deployment environments"""
    environments = await integration_service.get_deployment_environments(db, current_user.id)
    return environments
