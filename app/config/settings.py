"""
Application Settings Configuration
"""
import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    PROJECT_NAME: str = "TechSophy Keystone API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Authentication Mode - Switch between 'local' and 'keycloak'
    AUTH_MODE: str = "local"  # Changed to local for development testing

    # Local JWT Security (fallback/development)
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Keycloak Configuration
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "techsophy"
    KEYCLOAK_CLIENT_ID: str = "keystone-backend"
    KEYCLOAK_CLIENT_SECRET: str = ""
    KEYCLOAK_ADMIN_USERNAME: str = "admin"
    KEYCLOAK_ADMIN_PASSWORD: str = "admin"

    # Keycloak Security Settings
    KEYCLOAK_PUBLIC_KEY: Optional[str] = None
    KEYCLOAK_ALGORITHM: str = "RS256"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./keystone.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Google AI
    GOOGLE_AI_API_KEY: str = ""

    # CORS - Allow all origins for development
    BACKEND_CORS_ORIGINS: str = "*"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> str:
        if isinstance(v, str):
            return v
        elif isinstance(v, list):
            return ",".join(v)
        return "*"  # Default to allow all origins

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # AI Model settings
    DEFAULT_AI_MODEL: str = "gemini-2.0-flash-exp"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 2048

    class Config:
        case_sensitive = True
        env_file = ".env"

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get application settings (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
