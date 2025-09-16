"""
?Reports Generation Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.report import (
    ReportResponse, ReportGenerateRequest, ReportTemplate,
    ScheduledReportCreate, ScheduledReportResponse
)
from app.services.reports_service import reports_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ReportResponse])
async def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    report_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all reports"""
    reports = await reports_service.get_reports(db, current_user.id, skip, limit, report_type)
    return reports

@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    report_data: ReportGenerateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a new report"""
    report = await reports_service.generate_report(db, report_data, current_user.id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report generation failed"
        )
    return ReportResponse.from_orm(report)

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get report by ID"""
    report = await reports_service.get_report_by_id(db, report_id, current_user.id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return ReportResponse.from_orm(report)

@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete report"""
    success = await reports_service.delete_report(db, report_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return {"message": "Report deleted successfully"}

@router.get("/templates", response_model=List[ReportTemplate])
async def get_report_templates(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get available report templates"""
    templates = await reports_service.get_report_templates(db, current_user.id)
    return templates

@router.post("/schedule", response_model=ScheduledReportResponse)
async def schedule_report(
    schedule_data: ScheduledReportCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Schedule a report for automatic generation"""
    scheduled_report = await reports_service.schedule_report(db, schedule_data, current_user.id)
    if not scheduled_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report scheduling failed"
        )
    return ScheduledReportResponse.from_orm(scheduled_report)

@router.get("/scheduled", response_model=List[ScheduledReportResponse])
async def get_scheduled_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get scheduled reports"""
    scheduled_reports = await reports_service.get_scheduled_reports(db, current_user.id, skip, limit)
    return scheduled_reports
