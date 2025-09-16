"""
Authentication Dependencies
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.config.settings import get_settings
from app.services.auth_service import auth_service
from app.services.keycloak_auth_service import KeycloakAuthService
from app.models.user import User

settings = get_settings()
security = HTTPBearer()
keycloak_service = KeycloakAuthService() if settings.AUTH_MODE == "keycloak" else None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user - supports both local JWT and Keycloak"""
    token = credentials.credentials

    if settings.AUTH_MODE == "keycloak" and keycloak_service:
        # Keycloak authentication
        try:
            # Validate token with Keycloak
            payload = await keycloak_service.validate_token(token)

            # Get user info from Keycloak
            user_info = await keycloak_service.get_user_info(token)

            # Sync user to local database
            user = await keycloak_service.sync_user_to_local_db(user_info, db)

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Inactive user"
                )

            return user

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        # Local JWT authentication (fallback)
        payload = auth_service.verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user from database - user_id_str is already a string UUID
        user = await auth_service.get_user_by_id(db, user_id=user_id_str)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
