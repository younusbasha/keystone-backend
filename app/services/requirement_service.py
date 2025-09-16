"""
Requirement Service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
import structlog

from app.models.requirement import Requirement
from app.models.task import Task
from app.models.project import Project
from app.schemas.requirement import (
    RequirementCreate, RequirementUpdate, RequirementResponse,
    RequirementListResponse, RequirementAnalysisResponse
)
from app.schemas.task import TaskResponse
from app.services.gemini_service import gemini_service

logger = structlog.get_logger(__name__)

class RequirementService:
    """Service for managing requirements"""

    async def create_requirement(
        self,
        db: AsyncSession,
        requirement_data: RequirementCreate,
        user_id: str  # Changed to str for UUID
    ) -> Requirement:
        """Create a new requirement"""
        try:
            # Verify project ownership
            result = await db.execute(
                select(Project)
                .where(Project.id == requirement_data.project_id)
                .where(Project.owner_id == user_id)
                .where(Project.is_deleted == False)
            )
            project = result.scalar_one_or_none()

            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found or access denied"
                )

            db_requirement = Requirement(
                title=requirement_data.title,
                description=requirement_data.description,
                type=requirement_data.type,
                priority=requirement_data.priority,
                status=requirement_data.status,
                acceptance_criteria=requirement_data.acceptance_criteria,
                tags=requirement_data.tags,
                project_id=requirement_data.project_id,
                created_by=user_id
            )

            db.add(db_requirement)
            await db.commit()
            await db.refresh(db_requirement)

            logger.info("Requirement created successfully", requirement_id=db_requirement.id, user_id=user_id)
            return db_requirement

        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error("Failed to create requirement", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create requirement"
            )

    async def get_requirement_by_id(
        self,
        db: AsyncSession,
        requirement_id: str,  # Changed from int to str
        user_id: str  # Changed from int to str
    ) -> Optional[Requirement]:
        """Get requirement by ID with user access check"""
        try:
            result = await db.execute(
                select(Requirement)
                .join(Project)
                .options(selectinload(Requirement.tasks))
                .where(Requirement.id == requirement_id)
                .where(Project.owner_id == user_id)
                .where(Requirement.is_deleted == False)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Failed to get requirement", requirement_id=requirement_id, error=str(e))
            return None

    async def get_project_requirements(
        self,
        db: AsyncSession,
        project_id: str,  # Changed from int to str
        user_id: str,  # Changed from int to str
        skip: int = 0,
        limit: int = 20
    ) -> RequirementListResponse:
        """Get requirements for a project with pagination"""
        try:
            # Verify project ownership
            result = await db.execute(
                select(Project)
                .where(Project.id == project_id)
                .where(Project.owner_id == user_id)
                .where(Project.is_deleted == False)
            )
            project = result.scalar_one_or_none()

            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found or access denied"
                )

            # Get total count
            count_result = await db.execute(
                select(func.count(Requirement.id))
                .where(Requirement.project_id == project_id)
                .where(Requirement.is_deleted == False)
            )
            total = count_result.scalar()

            # Get requirements
            result = await db.execute(
                select(Requirement)
                .options(selectinload(Requirement.tasks))
                .where(Requirement.project_id == project_id)
                .where(Requirement.is_deleted == False)
                .offset(skip)
                .limit(limit)
                .order_by(Requirement.updated_at.desc())
            )
            requirements = result.scalars().all()

            # Convert to response format
            requirement_responses = [
                RequirementResponse(
                    id=req.id,
                    title=req.title,
                    description=req.description,
                    type=req.type,
                    priority=req.priority,
                    status=req.status,
                    acceptance_criteria=req.acceptance_criteria or [],
                    tags=req.tags or [],
                    project_id=req.project_id,
                    created_by=req.created_by,
                    created_at=req.created_at,
                    updated_at=req.updated_at,
                    ai_analysis=req.ai_analysis
                )
                for req in requirements
            ]

            return RequirementListResponse(
                requirements=requirement_responses,
                total=total,
                page=skip // limit + 1 if limit > 0 else 1,
                page_size=limit
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Failed to get project requirements", project_id=project_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve requirements"
            )

    async def get_user_requirements(
        self,
        db: AsyncSession,
        user_id: str,  # Changed to str for UUID
        skip: int = 0,
        limit: int = 20
    ) -> RequirementListResponse:
        """Get all requirements for a user across all their projects"""
        try:
            # Get total count
            count_result = await db.execute(
                select(func.count(Requirement.id))
                .join(Project)
                .where(Project.owner_id == user_id)
                .where(Requirement.is_deleted == False)
                .where(Project.is_deleted == False)
            )
            total = count_result.scalar()

            # Get requirements
            result = await db.execute(
                select(Requirement)
                .join(Project)
                .options(selectinload(Requirement.tasks))
                .where(Project.owner_id == user_id)
                .where(Requirement.is_deleted == False)
                .where(Project.is_deleted == False)
                .offset(skip)
                .limit(limit)
                .order_by(Requirement.updated_at.desc())
            )
            requirements = result.scalars().all()

            # Convert to response format
            requirement_responses = [
                RequirementResponse(
                    id=req.id,
                    title=req.title,
                    description=req.description,
                    type=req.type,
                    priority=req.priority,
                    status=req.status,
                    acceptance_criteria=req.acceptance_criteria or [],
                    tags=req.tags or [],
                    project_id=req.project_id,
                    created_by=req.created_by,
                    created_at=req.created_at,
                    updated_at=req.updated_at,
                    ai_analysis=req.ai_analysis
                )
                for req in requirements
            ]

            return RequirementListResponse(
                requirements=requirement_responses,
                total=total,
                page=skip // limit + 1 if limit > 0 else 1,
                page_size=limit
            )

        except Exception as e:
            logger.error("Failed to get user requirements", user_id=user_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve requirements"
            )

    async def update_requirement(
        self,
        db: AsyncSession,
        requirement_id: str,  # Changed from int to str
        requirement_data: RequirementUpdate,
        user_id: str  # Changed from int to str
    ) -> Optional[Requirement]:
        """Update a requirement"""
        try:
            # Get requirement with project ownership check
            result = await db.execute(
                select(Requirement)
                .join(Project)
                .where(Requirement.id == requirement_id)
                .where(Project.owner_id == user_id)
                .where(Requirement.is_deleted == False)
            )
            requirement = result.scalar_one_or_none()

            if not requirement:
                return None

            # Update fields
            update_data = requirement_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(requirement, field, value)

            await db.commit()
            await db.refresh(requirement)

            logger.info("Requirement updated successfully", requirement_id=requirement_id)
            return requirement

        except Exception as e:
            await db.rollback()
            logger.error("Failed to update requirement", requirement_id=requirement_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update requirement"
            )

    async def delete_requirement(self, db: AsyncSession, requirement_id: str, user_id: str) -> bool:
        """Soft delete a requirement"""
        try:
            result = await db.execute(
                select(Requirement)
                .join(Project)
                .where(Requirement.id == requirement_id)
                .where(Project.owner_id == user_id)
                .where(Requirement.is_deleted == False)
            )
            requirement = result.scalar_one_or_none()

            if not requirement:
                return False

            requirement.is_deleted = True
            await db.commit()

            logger.info("Requirement deleted successfully", requirement_id=requirement_id)
            return True

        except Exception as e:
            await db.rollback()
            logger.error("Failed to delete requirement", requirement_id=requirement_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete requirement"
            )

    async def analyze_requirements_batch(self, db: AsyncSession, requirement_ids: list[str], user_id: str) -> dict:
        """Analyze multiple requirements at once"""
        # Placeholder for batch analysis logic
        results = {}
        for req_id in requirement_ids:
            # In a real implementation, this would be a batch operation
            analysis = await self.analyze_requirement(db, req_id, user_id)
            results[req_id] = analysis
        return {"status": "batch analysis complete", "results": results}

    async def update_requirement_status(self, db: AsyncSession, requirement_id: str, status: str, user_id: str) -> bool:
        """Update requirement status"""
        requirement = await self.get_requirement_by_id(db, requirement_id, user_id)
        if not requirement:
            return False
        requirement.status = status
        await db.commit()
        return True

    async def get_requirement_history(self, db: AsyncSession, requirement_id: str, user_id: str) -> list:
        """Get requirement change history"""
        # Placeholder for history logic (e.g., from an audit table)
        return [{"timestamp": "2025-09-17T10:00:00Z", "user": user_id, "action": "created"},
                {"timestamp": "2025-09-17T11:00:00Z", "user": user_id, "action": "updated status to 'approved'"}]

    async def approve_requirement(self, db: AsyncSession, requirement_id: str, user_id: str) -> bool:
        """Approve a requirement"""
        return await self.update_requirement_status(db, requirement_id, "approved", user_id)

    async def reject_requirement(self, db: AsyncSession, requirement_id: str, rejection_reason: str, user_id: str) -> bool:
        """Reject a requirement"""
        # You might want to store the rejection_reason somewhere
        return await self.update_requirement_status(db, requirement_id, "rejected", user_id)

    async def analyze_requirement(
        self,
        db: AsyncSession,
        requirement_id: str,  # Changed from int to str
        user_id: str  # Changed from int to str
    ) -> RequirementAnalysisResponse:
        """Analyze requirement with AI"""
        try:
            # Get requirement
            requirement = await self.get_requirement_by_id(db, requirement_id, user_id)
            if not requirement:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Requirement not found or access denied"
                )

            # Perform AI analysis
            analysis = await gemini_service.analyze_requirement(requirement.description)

            # Update requirement with analysis
            requirement.ai_analysis = analysis
            await db.commit()

            logger.info("Requirement analysis completed", requirement_id=requirement_id)
            return RequirementAnalysisResponse(
                requirement_id=requirement_id,
                analysis=analysis,
                confidence_score=analysis.get("confidence_score", 0.0),
                analyzed_at=requirement.updated_at
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Failed to analyze requirement", requirement_id=requirement_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to analyze requirement"
            )

    async def generate_tasks(
        self,
        db: AsyncSession,
        requirement_id: str,  # Changed from int to str
        user_id: str  # Changed from int to str
    ) -> List[TaskResponse]:
        """Generate tasks from requirement analysis"""
        try:
            # Get requirement
            requirement = await self.get_requirement_by_id(db, requirement_id, user_id)
            if not requirement:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Requirement not found or access denied"
                )

            # Generate tasks using AI
            requirement_data = {
                "title": requirement.title,
                "description": requirement.description,
                "ai_analysis": requirement.ai_analysis or {}
            }

            tasks_data = await gemini_service.generate_tasks(requirement_data)

            # Create task records
            created_tasks = []
            for task_data in tasks_data:
                db_task = Task(
                    title=task_data.get("title", "Untitled Task"),
                    description=task_data.get("description", ""),
                    type=task_data.get("type", "feature"),
                    priority=task_data.get("priority", "medium"),
                    estimated_hours=task_data.get("estimated_hours"),
                    dependencies=task_data.get("dependencies", []),
                    acceptance_criteria=task_data.get("acceptance_criteria", []),
                    requirement_id=requirement_id
                )
                db.add(db_task)
                created_tasks.append(db_task)

            await db.commit()

            # Refresh and convert to response format
            task_responses = []
            for task in created_tasks:
                await db.refresh(task)
                task_response = TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    type=task.type,
                    priority=task.priority,
                    estimated_hours=task.estimated_hours,
                    dependencies=task.dependencies or [],
                    acceptance_criteria=task.acceptance_criteria or [],
                    requirement_id=task.requirement_id,
                    created_at=task.created_at,
                    updated_at=task.updated_at
                )
                task_responses.append(task_response)

            logger.info("Tasks generated successfully", requirement_id=requirement_id, task_count=len(task_responses))
            return task_responses

        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error("Failed to generate tasks", requirement_id=requirement_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate tasks"
            )

# Global requirement service instance
requirement_service = RequirementService()
