"""
Authentication Service
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog
import uuid

from app.config.settings import get_settings
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token

settings = get_settings()
logger = structlog.get_logger(__name__)

class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create an access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        """Create a refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None
    
    async def authenticate_user(self, db: AsyncSession, username: str, password: str) -> Optional[User]:
        """Authenticate user with username/email and password"""
        try:
            # Try to find user by username or email
            result = await db.execute(
                select(User).where(
                    (User.username == username) | (User.email == username)
                )
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            if not self.verify_password(password, user.password_hash):
                return None

            return user
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None

    async def create_user(self, db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            # Check if user already exists
            result = await db.execute(
                select(User).where(
                    (User.email == user_data.email) | (User.username == user_data.username)
                )
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                if existing_user.email == user_data.email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already taken"
                    )
            
            # Create new user
            hashed_password = self.get_password_hash(user_data.password)
            db_user = User(
                id=str(uuid.uuid4()),
                email=user_data.email,
                username=user_data.username,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                bio=user_data.bio,
                avatar_url=user_data.avatar_url,
                password_hash=hashed_password,
                is_active=True,
                is_verified=False
            )
            
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            
            return db_user
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"User creation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {str(e)}"
            )

    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get all users"""
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_user_by_id(self, db: AsyncSession, user_id: str):
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update_user(self, db: AsyncSession, user_id: str, user_data):
        """Update user"""
        try:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return None

            # Update fields
            if hasattr(user_data, 'first_name') and user_data.first_name:
                user.first_name = user_data.first_name
            if hasattr(user_data, 'last_name') and user_data.last_name:
                user.last_name = user_data.last_name
            if hasattr(user_data, 'bio') and user_data.bio:
                user.bio = user_data.bio
            if hasattr(user_data, 'avatar_url') and user_data.avatar_url:
                user.avatar_url = user_data.avatar_url

            await db.commit()
            await db.refresh(user)
            return user
        except Exception as e:
            await db.rollback()
            logger.error(f"User update error: {str(e)}")
            return None

    async def delete_user(self, db: AsyncSession, user_id: str):
        """Delete user"""
        try:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return False

            await db.delete(user)
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            logger.error(f"User deletion error: {str(e)}")
            return False

    async def change_password(self, db: AsyncSession, user_id: str, current_password: str, new_password: str):
        """Change user password"""
        try:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return False

            if not self.verify_password(current_password, user.password_hash):
                return False

            user.password_hash = self.get_password_hash(new_password)
            await db.commit()
            return True
        except Exception:
            await db.rollback()
            return False

    async def initiate_password_reset(self, db: AsyncSession, email: str):
        """Initiate password reset"""
        # Placeholder implementation
        return {"message": "Password reset initiated"}

    async def reset_password(self, db: AsyncSession, token: str, new_password: str):
        """Reset password with token"""
        # Placeholder implementation
        return True
```
