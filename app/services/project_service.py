"""
Project Service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
import structlog

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse

logger = structlog.get_logger(__name__)

class ProjectService:
    """Service for managing projects"""

    async def create_project(self, db: AsyncSession, project_data: ProjectCreate, owner_id: int) -> Project:
        """Create a new project"""
        try:
            db_project = Project(
                name=project_data.name,
                description=project_data.description,
                status=project_data.status,
                priority=project_data.priority,
                start_date=project_data.start_date,
                end_date=project_data.end_date,
                budget=project_data.budget,
                owner_id=owner_id
            )
            
            db.add(db_project)
            await db.commit()
            await db.refresh(db_project)
            
            logger.info("Project created successfully", project_id=db_project.id, owner_id=owner_id)
            return db_project
            
        except Exception as e:
            await db.rollback()
            logger.error("Failed to create project", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create project"
            )

    async def get_project_by_id(self, db: AsyncSession, project_id: int, user_id: int) -> Optional[Project]:
        """Get project by ID with user access check"""
        try:
            result = await db.execute(
                select(Project)
                .options(selectinload(Project.requirements))
                .where(Project.id == project_id)
                .where(Project.owner_id == user_id)
                .where(Project.is_deleted == False)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Failed to get project", project_id=project_id, error=str(e))
            return None

    async def get_user_projects(
        self, 
        db: AsyncSession, 
        user_id: str,  # Changed from int to str
        skip: int = 0,
        limit: int = 20
    ) -> ProjectListResponse:
        """Get projects for a user with pagination"""
        try:
            # Get total count
            count_result = await db.execute(
                select(func.count(Project.id))
                .where(Project.owner_id == user_id)
                .where(Project.is_deleted == False)
            )
            total = count_result.scalar()

            # Get projects
            result = await db.execute(
                select(Project)
                .options(selectinload(Project.requirements))
                .where(Project.owner_id == user_id)
                .where(Project.is_deleted == False)
                .offset(skip)
                .limit(limit)
                .order_by(Project.updated_at.desc())
            )
            projects = result.scalars().all()

            # Convert to response format
            project_responses = []
            for project in projects:
                project_response = ProjectResponse(
                    id=project.id,
                    name=project.name,
                    description=project.description,
                    status=project.status,
                    priority=project.priority,
                    start_date=project.start_date,
                    end_date=project.end_date,
                    budget=project.budget,
                    owner_id=project.owner_id,
                    created_at=project.created_at,
                    updated_at=project.updated_at,
                    requirements_count=len(project.requirements)
                )
                project_responses.append(project_response)

            return ProjectListResponse(
                projects=project_responses,
                total=total,
                page=skip // limit + 1 if limit > 0 else 1,
                page_size=limit
            )

        except Exception as e:
            logger.error("Failed to get user projects", user_id=user_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve projects"
            )

    async def update_project(
        self, 
        db: AsyncSession, 
        project_id: str,  # Changed from int to str
        project_data: ProjectUpdate,
        user_id: str  # Changed from int to str
    ) -> Optional[Project]:
        """Update a project"""
        try:
            # Get project
            result = await db.execute(
                select(Project)
                .where(Project.id == project_id)
                .where(Project.owner_id == user_id)
                .where(Project.is_deleted == False)
            )
            project = result.scalar_one_or_none()
            
            if not project:
                return None

            # Update fields
            update_data = project_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(project, field, value)

            await db.commit()
            await db.refresh(project)
            
            logger.info("Project updated successfully", project_id=project_id)
            return project

        except Exception as e:
            await db.rollback()
            logger.error("Failed to update project", project_id=project_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update project"
            )

    async def delete_project(self, db: AsyncSession, project_id: str, user_id: str) -> bool:  # Changed both to str
        """Soft delete a project"""
        try:
            result = await db.execute(
                select(Project)
                .where(Project.id == project_id)
                .where(Project.owner_id == user_id)
                .where(Project.is_deleted == False)
            )
            project = result.scalar_one_or_none()
            
            if not project:
                return False

            project.is_deleted = True
            await db.commit()
            
            logger.info("Project deleted successfully", project_id=project_id)
            return True

        except Exception as e:
            await db.rollback()
            logger.error("Failed to delete project", project_id=project_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete project"
            )

    async def get_project_stats(self, db: AsyncSession, project_id: str, user_id: str) -> Optional[dict]:
        """Get project statistics"""
        project = await self.get_project_by_id(db, project_id, user_id)
        if not project:
            return None
        # Placeholder for stats logic
        return {"requirements_count": len(project.requirements), "status": project.status, "budget": project.budget}

    async def get_project_team(self, db: AsyncSession, project_id: str, user_id: str) -> list:
        """Get project team members"""
        # Placeholder for team logic
        return [{"user_id": user_id, "role": "owner"}]

    async def add_team_member(self, db: AsyncSession, project_id: str, new_user_id: str, role: str, current_user_id: str) -> bool:
        """Add a team member to a project"""
        # Placeholder for add team member logic
        return True

    async def remove_team_member(self, db: AsyncSession, project_id: str, user_to_remove_id: str, current_user_id: str) -> bool:
        """Remove a team member from a project"""
        # Placeholder for remove team member logic
        return True

    async def update_project_status(self, db: AsyncSession, project_id: str, status: str, user_id: str) -> bool:
        """Update project status"""
        project = await self.get_project_by_id(db, project_id, user_id)
        if not project:
            return False
        project.status = status
        await db.commit()
        return True

    async def get_project_timeline(self, db: AsyncSession, project_id: str, user_id: str) -> Optional[dict]:
        """Get project timeline"""
        project = await self.get_project_by_id(db, project_id, user_id)
        if not project:
            return None
        # Placeholder for timeline logic
        return {"start_date": project.start_date, "end_date": project.end_date, "events": []}

# Global project service instance
project_service = ProjectService()
