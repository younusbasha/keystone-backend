"""
Keycloak Authentication Service
"""
import httpx
import jwt
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from app.config.settings import get_settings
from app.models.user import User
from app.schemas.user import UserResponse

settings = get_settings()
logger = structlog.get_logger(__name__)


class KeycloakAuthService:
    """Keycloak authentication service"""

    def __init__(self):
        self.keycloak_url = settings.KEYCLOAK_URL
        self.realm = settings.KEYCLOAK_REALM
        self.client_id = settings.KEYCLOAK_CLIENT_ID
        self.client_secret = settings.KEYCLOAK_CLIENT_SECRET
        self.admin_username = settings.KEYCLOAK_ADMIN_USERNAME
        self.admin_password = settings.KEYCLOAK_ADMIN_PASSWORD

        # Keycloak endpoints
        self.auth_url = f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect"
        self.admin_url = f"{self.keycloak_url}/admin/realms/{self.realm}"
        self.token_endpoint = f"{self.auth_url}/token"
        self.userinfo_endpoint = f"{self.auth_url}/userinfo"
        self.jwks_endpoint = f"{self.auth_url}/certs"

        # Cache for JWK public keys
        self._jwks_cache = None
        self._admin_token_cache = None

    async def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user with Keycloak"""
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    "grant_type": "password",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "username": username,
                    "password": password,
                    "scope": "openid profile email"
                }

                response = await client.post(self.token_endpoint, data=data)

                if response.status_code == 200:
                    token_data = response.json()
                    return {
                        "access_token": token_data["access_token"],
                        "refresh_token": token_data["refresh_token"],
                        "expires_in": token_data["expires_in"],
                        "token_type": token_data["token_type"]
                    }
                elif response.status_code == 401:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid username or password"
                    )
                else:
                    logger.error(f"Keycloak authentication failed: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Authentication service error"
                    )
        except httpx.RequestError as e:
            logger.error(f"Keycloak connection error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    "grant_type": "refresh_token",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token
                }

                response = await client.post(self.token_endpoint, data=data)

                if response.status_code == 200:
                    token_data = response.json()
                    return {
                        "access_token": token_data["access_token"],
                        "refresh_token": token_data.get("refresh_token", refresh_token),
                        "expires_in": token_data["expires_in"],
                        "token_type": token_data["token_type"]
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid refresh token"
                    )
        except httpx.RequestError as e:
            logger.error(f"Keycloak token refresh error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """Validate JWT token with Keycloak"""
        try:
            # Get JWKs for token validation
            jwks = await self._get_jwks()

            # Decode token header to get kid
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            # Find the correct key
            key = None
            for jwk in jwks["keys"]:
                if jwk["kid"] == kid:
                    key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
                    break

            if not key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token signature"
                )

            # Validate token
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=f"{self.keycloak_url}/realms/{self.realm}"
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"Token validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    async def get_user_info(self, token: str) -> Dict[str, Any]:
        """Get user information from Keycloak"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(self.userinfo_endpoint, headers=headers)

                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token"
                    )
        except httpx.RequestError as e:
            logger.error(f"Keycloak userinfo error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user in Keycloak"""
        try:
            admin_token = await self._get_admin_token()

            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {admin_token}",
                    "Content-Type": "application/json"
                }

                keycloak_user = {
                    "username": user_data["username"],
                    "email": user_data["email"],
                    "firstName": user_data["first_name"],
                    "lastName": user_data["last_name"],
                    "enabled": True,
                    "emailVerified": False,
                    "credentials": [{
                        "type": "password",
                        "value": user_data["password"],
                        "temporary": False
                    }]
                }

                response = await client.post(
                    f"{self.admin_url}/users",
                    headers=headers,
                    json=keycloak_user
                )

                if response.status_code == 201:
                    # Get user ID from location header
                    location = response.headers.get("Location")
                    user_id = location.split("/")[-1] if location else None

                    return {
                        "id": user_id,
                        "username": user_data["username"],
                        "email": user_data["email"],
                        "first_name": user_data["first_name"],
                        "last_name": user_data["last_name"]
                    }
                elif response.status_code == 409:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="User already exists"
                    )
                else:
                    logger.error(f"Keycloak user creation failed: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="User creation failed"
                    )

        except httpx.RequestError as e:
            logger.error(f"Keycloak user creation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )

    async def logout_user(self, refresh_token: str) -> bool:
        """Logout user (invalidate refresh token)"""
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token
                }

                response = await client.post(
                    f"{self.auth_url}/logout",
                    data=data
                )

                return response.status_code == 204

        except httpx.RequestError as e:
            logger.error(f"Keycloak logout error: {e}")
            return False

    async def sync_user_to_local_db(self, keycloak_user: Dict[str, Any], db: AsyncSession) -> User:
        """Sync Keycloak user to local database"""
        # Check if user exists in local DB
        query = select(User).where(User.email == keycloak_user["email"])
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            # Create new user in local DB
            user = User(
                email=keycloak_user["email"],
                username=keycloak_user["preferred_username"],
                first_name=keycloak_user.get("given_name", ""),
                last_name=keycloak_user.get("family_name", ""),
                hashed_password="",  # Not needed for Keycloak users
                is_active=True,
                is_verified=keycloak_user.get("email_verified", False)
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            # Update existing user
            user.first_name = keycloak_user.get("given_name", user.first_name)
            user.last_name = keycloak_user.get("family_name", user.last_name)
            user.is_verified = keycloak_user.get("email_verified", user.is_verified)
            await db.commit()

        return user

    async def _get_jwks(self) -> Dict[str, Any]:
        """Get JWKs from Keycloak for token validation"""
        if not self._jwks_cache:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(self.jwks_endpoint)
                    self._jwks_cache = response.json()
            except httpx.RequestError as e:
                logger.error(f"Failed to get JWKs: {e}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Authentication service unavailable"
                )

        return self._jwks_cache

    async def _get_admin_token(self) -> str:
        """Get admin token for Keycloak admin operations"""
        if not self._admin_token_cache:
            try:
                async with httpx.AsyncClient() as client:
                    data = {
                        "grant_type": "password",
                        "client_id": "admin-cli",
                        "username": self.admin_username,
                        "password": self.admin_password
                    }

                    response = await client.post(
                        f"{self.keycloak_url}/realms/master/protocol/openid-connect/token",
                        data=data
                    )

                    if response.status_code == 200:
                        token_data = response.json()
                        self._admin_token_cache = token_data["access_token"]
                    else:
                        raise Exception("Failed to get admin token")

            except Exception as e:
                logger.error(f"Failed to get admin token: {e}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Authentication service unavailable"
                )

        return self._admin_token_cache
