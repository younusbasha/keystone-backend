"""
Dashboard & Analytics Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.dashboard import (
    DashboardOverview, DashboardStats, DashboardMetrics,
    ActivityFeed, NotificationResponse, WidgetCreate,
    WidgetUpdate, WidgetResponse, AnalyticsTrends, AnalyticsReports
)
from app.services.dashboard_service import dashboard_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard overview"""
    overview = await dashboard_service.get_dashboard_overview(db, current_user.id)
    return overview

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics"""
    stats = await dashboard_service.get_dashboard_stats(db, current_user.id)
    return stats

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard metrics"""
    metrics = await dashboard_service.get_dashboard_metrics(db, current_user.id)
    return metrics

@router.get("/activity", response_model=List[ActivityFeed])
async def get_dashboard_activity(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard activity"""
    activity = await dashboard_service.get_dashboard_activity(db, current_user.id, skip, limit)
    return activity

@router.get("/activity-feed", response_model=List[ActivityFeed])
async def get_dashboard_activity_feed(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard activity feed"""
    feed = await dashboard_service.get_dashboard_activity_feed(db, current_user.id, skip, limit)
    return feed

@router.get("/metrics/automation", response_model=DashboardMetrics)
async def get_automation_metrics(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get automation metrics"""
    metrics = await dashboard_service.get_automation_metrics(db, current_user.id)
    return metrics

@router.get("/metrics/projects", response_model=DashboardMetrics)
async def get_projects_metrics(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get projects metrics"""
    metrics = await dashboard_service.get_projects_metrics(db, current_user.id)
    return metrics

@router.get("/metrics/performance", response_model=DashboardMetrics)
async def get_performance_metrics(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get performance metrics"""
    metrics = await dashboard_service.get_performance_metrics(db, current_user.id)
    return metrics

@router.get("/analytics/trends", response_model=AnalyticsTrends)
async def get_analytics_trends(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics trends"""
    trends = await dashboard_service.get_analytics_trends(db, current_user.id, days)
    return trends

@router.get("/analytics/reports", response_model=AnalyticsReports)
async def get_analytics_reports(
    report_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics reports"""
    reports = await dashboard_service.get_analytics_reports(db, current_user.id, report_type)
    return reports

# Notifications

@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user notifications"""
    notifications = await dashboard_service.get_notifications(db, current_user.id, skip, limit, unread_only)
    return notifications

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark notification as read"""
    success = await dashboard_service.mark_notification_read(db, notification_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return {"message": "Notification marked as read"}

@router.post("/notifications/mark-all-read")
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark all notifications as read"""
    count = await dashboard_service.mark_all_notifications_read(db, current_user.id)
    return {"message": f"Marked {count} notifications as read"}

# Widgets

@router.get("/widgets", response_model=List[WidgetResponse])
async def get_widgets(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard widgets"""
    widgets = await dashboard_service.get_widgets(db, current_user.id)
    return widgets

@router.post("/widgets", response_model=WidgetResponse, status_code=status.HTTP_201_CREATED)
async def create_widget(
    widget_data: WidgetCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create dashboard widget"""
    widget = await dashboard_service.create_widget(db, widget_data, current_user.id)
    return WidgetResponse.from_orm(widget)

@router.put("/widgets/{widget_id}", response_model=WidgetResponse)
async def update_widget(
    widget_id: int,
    widget_data: WidgetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update dashboard widget"""
    widget = await dashboard_service.update_widget(db, widget_id, widget_data, current_user.id)
    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found"
        )
    return WidgetResponse.from_orm(widget)

@router.delete("/widgets/{widget_id}")
async def delete_widget(
    widget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete dashboard widget"""
    success = await dashboard_service.delete_widget(db, widget_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found"
        )
    return {"message": "Widget deleted successfully"}
