"""
Custom Middleware Components
"""
import time
import uuid
from typing import Dict, Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
import structlog
from collections import defaultdict
from datetime import datetime, timedelta

logger = structlog.get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        request_id = str(uuid.uuid4())

        # Add request ID to request state
        request.state.request_id = request_id

        # Log request
        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            user_agent=request.headers.get("user-agent"),
            client_ip=request.client.host if request.client else None,
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration = time.time() - start_time
            logger.error(
                "Request failed",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                duration=duration,
                error=str(exc),
            )
            raise

        # Log response
        duration = time.time() - start_time
        logger.info(
            "Request completed",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            duration=duration,
        )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware"""

    def __init__(self, app, calls: int = 60, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, list] = defaultdict(list)

    def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting"""
        # Use IP address as client identifier
        return request.client.host if request.client else "unknown"

    def _cleanup_old_requests(self, client_requests: list, now: datetime):
        """Remove old requests outside the time window"""
        cutoff = now - timedelta(seconds=self.period)
        return [req_time for req_time in client_requests if req_time > cutoff]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health check and documentation endpoints
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        client_id = self._get_client_id(request)
        now = datetime.now()

        # Clean up old requests
        self.clients[client_id] = self._cleanup_old_requests(
            self.clients[client_id], now
        )

        # Check rate limit
        if len(self.clients[client_id]) >= self.calls:
            logger.warning(
                "Rate limit exceeded",
                client_id=client_id,
                requests_count=len(self.clients[client_id]),
                limit=self.calls,
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded: {self.calls} requests per {self.period} seconds",
                    "retry_after": self.period
                },
                headers={"Retry-After": str(self.period)}
            )

        # Record this request
        self.clients[client_id].append(now)

        return await call_next(request)
