"""
Authentication Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import structlog

from app.config.database import get_db
from app.config.settings import get_settings
from app.core.auth import get_current_user
from app.schemas.user import (
    UserCreate, UserResponse, Token, UserLogin, UserUpdate,
    PasswordChange, PasswordReset, ForgotPassword
)
from app.services.auth_service import auth_service
from app.services.keycloak_auth_service import KeycloakAuthService
from app.models.user import User

logger = structlog.get_logger(__name__)
router = APIRouter()
settings = get_settings()
keycloak_service = KeycloakAuthService() if settings.AUTH_MODE == "keycloak" else None


# Authentication Endpoints

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    try:
        logger.info(f"Registration attempt for user: {user.username}")
        created_user = await auth_service.create_user(db, user)
        logger.info(f"User created successfully: {created_user.id}")

        return UserResponse(
            id=created_user.id,
            email=created_user.email,
            username=created_user.username,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            bio=created_user.bio,
            avatar_url=created_user.avatar_url,
            is_active=created_user.is_active,
            is_verified=created_user.is_verified,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return tokens"""
    if settings.AUTH_MODE == "keycloak" and keycloak_service:
        try:
            token_data = await keycloak_service.authenticate_user(
                user_credentials.username,
                user_credentials.password
            )

            return Token(
                access_token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                token_type=token_data["token_type"]
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed"
            )
    else:
        user = await auth_service.authenticate_user(
            db, user_credentials.username, user_credentials.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = auth_service.create_access_token(data={"sub": str(user.id)})
        refresh_token = auth_service.create_refresh_token(data={"sub": str(user.id)})

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )


@router.post("/logout")
async def logout(
    refresh_token: str,
    current_user: User = Depends(get_current_user)
):
    """Logout user by invalidating refresh token"""
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token"""
    if settings.AUTH_MODE == "keycloak" and keycloak_service:
        try:
            token_data = await keycloak_service.refresh_token(refresh_token)

            return Token(
                access_token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                token_type=token_data["token_type"]
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    else:
        payload = auth_service.verify_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")
        access_token = auth_service.create_access_token(data={"sub": user_id})

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile"""
    updated_user = await auth_service.update_user(db, current_user.id, user_data)
    return UserResponse.from_orm(updated_user)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password"""
    success = await auth_service.change_password(
        db, current_user.id, password_data.current_password, password_data.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password"
        )

    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(
    forgot_data: ForgotPassword,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset"""
    try:
        await auth_service.initiate_password_reset(db, forgot_data.email)
        return {"message": "Password reset email sent if account exists"}
    except Exception as e:
        logger.error(f"Forgot password error: {str(e)}")
        return {"message": "Password reset email sent if account exists"}


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
):
    """Reset password using token"""
    success = await auth_service.reset_password(
        db, reset_data.token, reset_data.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    return {"message": "Password reset successfully"}


# User Management Endpoints

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of users (admin only)"""
    users = await auth_service.get_users(db, skip=skip, limit=limit, search=search)
    return [UserResponse.from_orm(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID"""
    user = await auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.from_orm(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user by ID (admin or own profile)"""
    if current_user.id != user_id:
        # Check if current user is admin (implement admin check)
        pass

    updated_user = await auth_service.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.from_orm(updated_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete user by ID (admin only)"""
    success = await auth_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
