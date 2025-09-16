"""
Task Management Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate,
    TaskComment, TaskCommentResponse, TaskAssignment,
    TaskTimeLog, TaskTimeLogResponse, TaskAttachment
)
from app.services.task_service import task_service
from app.core.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new task"""
    task = await task_service.create_task(db, task_data, current_user.id)
    return TaskResponse.from_orm(task)

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get tasks with filters"""
    tasks = await task_service.get_tasks(
        db, current_user.id, skip, limit, project_id, status, assigned_to
    )
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get task by ID"""
    task = await task_service.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse.from_orm(task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update task"""
    task = await task_service.update_task(db, task_id, task_data, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse.from_orm(task)

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete task"""
    success = await task_service.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}

@router.put("/{task_id}/status")
async def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update task status"""
    task = await task_service.update_task_status(db, task_id, status_data.status, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task status updated successfully", "status": task.status}

@router.post("/{task_id}/start")
async def start_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Start task"""
    success = await task_service.start_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or cannot be started"
        )
    return {"message": "Task started successfully"}

@router.post("/{task_id}/complete")
async def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Complete task"""
    success = await task_service.complete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or cannot be completed"
        )
    return {"message": "Task completed successfully"}

@router.post("/{task_id}/pause")
async def pause_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Pause task"""
    success = await task_service.pause_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or cannot be paused"
        )
    return {"message": "Task paused successfully"}

@router.post("/{task_id}/resume")
async def resume_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Resume task"""
    success = await task_service.resume_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or cannot be resumed"
        )
    return {"message": "Task resumed successfully"}

# Task Comments

@router.get("/{task_id}/comments", response_model=List[TaskCommentResponse])
async def get_task_comments(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get task comments"""
    comments = await task_service.get_task_comments(db, task_id, current_user.id)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return comments

@router.post("/{task_id}/comments", response_model=TaskCommentResponse)
async def create_task_comment(
    task_id: int,
    comment_data: TaskComment,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create task comment"""
    comment = await task_service.create_task_comment(db, task_id, comment_data, current_user.id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskCommentResponse.from_orm(comment)

@router.put("/{task_id}/comments/{comment_id}", response_model=TaskCommentResponse)
async def update_task_comment(
    task_id: int,
    comment_id: int,
    comment_data: TaskComment,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update task comment"""
    comment = await task_service.update_task_comment(db, task_id, comment_id, comment_data, current_user.id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or comment not found"
        )
    return TaskCommentResponse.from_orm(comment)

@router.delete("/{task_id}/comments/{comment_id}")
async def delete_task_comment(
    task_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete task comment"""
    success = await task_service.delete_task_comment(db, task_id, comment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or comment not found"
        )
    return {"message": "Comment deleted successfully"}

# Task Assignment

@router.post("/{task_id}/assign")
async def assign_task(
    task_id: int,
    assignment_data: TaskAssignment,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Assign task to user"""
    success = await task_service.assign_task(db, task_id, assignment_data.user_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or user not found"
        )
    return {"message": "Task assigned successfully"}

@router.post("/{task_id}/unassign")
async def unassign_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Unassign task"""
    success = await task_service.unassign_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task unassigned successfully"}

# Time Logs

@router.get("/{task_id}/time-logs", response_model=List[TaskTimeLogResponse])
async def get_task_time_logs(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get task time logs"""
    time_logs = await task_service.get_task_time_logs(db, task_id, current_user.id)
    if time_logs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return time_logs

@router.post("/{task_id}/time-logs", response_model=TaskTimeLogResponse)
async def create_time_log(
    task_id: int,
    time_log_data: TaskTimeLog,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create time log entry"""
    time_log = await task_service.create_time_log(db, task_id, time_log_data, current_user.id)
    if not time_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskTimeLogResponse.from_orm(time_log)

@router.put("/{task_id}/time-logs/{log_id}", response_model=TaskTimeLogResponse)
async def update_time_log(
    task_id: int,
    log_id: int,
    time_log_data: TaskTimeLog,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update time log entry"""
    time_log = await task_service.update_time_log(db, task_id, log_id, time_log_data, current_user.id)
    if not time_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or time log not found"
        )
    return TaskTimeLogResponse.from_orm(time_log)

# Task Attachments

@router.get("/{task_id}/attachments", response_model=List[TaskAttachment])
async def get_task_attachments(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get task attachments"""
    attachments = await task_service.get_task_attachments(db, task_id, current_user.id)
    if attachments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return attachments

@router.post("/{task_id}/attachments")
async def upload_task_attachment(
    task_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload task attachment"""
    attachment = await task_service.upload_task_attachment(db, task_id, file, current_user.id)
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or upload failed"
        )
    return {"message": "Attachment uploaded successfully", "attachment": attachment}

@router.delete("/{task_id}/attachments/{attachment_id}")
async def delete_task_attachment(
    task_id: int,
    attachment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete task attachment"""
    success = await task_service.delete_task_attachment(db, task_id, attachment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or attachment not found"
        )
    return {"message": "Attachment deleted successfully"}
