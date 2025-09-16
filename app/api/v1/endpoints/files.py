"""
File Management Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.file import (
    FileResponse, FileUploadResponse, BulkUploadResponse
)
from app.services.file_service import file_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    project_id: Optional[int] = Query(None),
    task_id: Optional[int] = Query(None),
    description: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload a single file"""
    result = await file_service.upload_file(db, file, current_user.id, project_id, task_id, description)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File upload failed"
        )
    return result

@router.get("/{file_id}", response_model=FileResponse)
async def get_file_info(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get file information by ID"""
    file_info = await file_service.get_file_by_id(db, file_id, current_user.id)
    if not file_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    return FileResponse.from_orm(file_info)

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete file by ID"""
    success = await file_service.delete_file(db, file_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    return {"message": "File deleted successfully"}

@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Download file by ID"""
    file_stream = await file_service.download_file(db, file_id, current_user.id)
    if not file_stream:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return StreamingResponse(
        file_stream["content"],
        media_type=file_stream["media_type"],
        headers={"Content-Disposition": f"attachment; filename={file_stream['filename']}"}
    )

@router.post("/bulk-upload", response_model=BulkUploadResponse)
async def bulk_upload_files(
    files: List[UploadFile] = File(...),
    project_id: Optional[int] = Query(None),
    task_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload multiple files"""
    result = await file_service.bulk_upload_files(db, files, current_user.id, project_id, task_id)
    return result

@router.get("/project/{project_id}", response_model=List[FileResponse])
async def get_project_files(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get files associated with a project"""
    files = await file_service.get_project_files(db, project_id, current_user.id, skip, limit)
    if files is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return files

@router.get("/task/{task_id}", response_model=List[FileResponse])
async def get_task_files(
    task_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get files associated with a task"""
    files = await file_service.get_task_files(db, task_id, current_user.id, skip, limit)
    if files is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return files
