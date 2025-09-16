"""
File Management Schemas
"""
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class FileResponse(BaseModel):
    """File response schema"""
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class BulkUploadResponse(BaseModel):
    """Bulk upload response schema"""
    uploaded_files: List[FileResponse]
    failed_files: List[dict] = []
    total_uploaded: int
    total_failed: int
