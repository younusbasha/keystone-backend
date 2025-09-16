"""
API v1 Router
"""
from fastapi import APIRouter

# Import endpoint routers
from app.api.v1.endpoints import (
    auth, projects, requirements, tasks, agents, integrations, dashboard,
    search, audit, admin, files, permissions, reports
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(auth.router, prefix="/users", tags=["Users"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(requirements.router, prefix="/requirements", tags=["Requirements"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(agents.router, prefix="/agents", tags=["AI Agents"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations & Deployments"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard & Analytics"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit & Logging"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"])
api_router.include_router(files.router, prefix="/files", tags=["File Management"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["Permissions & Roles"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])

@api_router.get("/")
async def api_root():
    """API v1 root endpoint"""
    return {
        "message": "TechSophy Keystone API v1",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth - Authentication & User Management",
            "users": "/users - User Operations",
            "projects": "/projects - Project Management",
            "requirements": "/requirements - Requirements Management",
            "tasks": "/tasks - Task Management",
            "agents": "/agents - AI Agents Management",
            "integrations": "/integrations - Integrations & Deployments",
            "dashboard": "/dashboard - Dashboard & Analytics",
            "search": "/search - Search Functionality",
            "audit": "/audit - Audit & Logging",
            "admin": "/admin - System Administration",
            "files": "/files - File Management",
            "permissions": "/permissions - Permissions & Roles",
            "reports": "/reports - Reports Generation"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }
