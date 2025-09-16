"""
Report Management Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class ReportResponse(BaseModel):
    """Report response schema"""
    id: int
    name: str
    type: str
    format: str = "pdf"
    status: str = "pending"
    file_path: Optional[str] = None
    parameters: Dict[str, Any] = {}
    generated_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class ReportGenerate(BaseModel):
    """Report generate schema"""
    type: str
    name: Optional[str] = None
    format: str = "pdf"
    project_id: Optional[int] = None
    parameters: Dict[str, Any] = {}

class ReportTemplate(BaseModel):
    """Report template schema"""
    id: int
    name: str
    type: str
    description: str
    parameters: Dict[str, Any] = {}

class ScheduledReport(BaseModel):
    """Scheduled report schema"""
    id: int
    name: str
    type: str
    schedule: str  # cron expression
    recipients: List[str]
    parameters: Dict[str, Any] = {}
    next_run: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReportSchedule(BaseModel):
    """Report schedule schema"""
    name: str
    type: str
    schedule: str  # cron expression
    recipients: List[str]
    parameters: Dict[str, Any] = {}
