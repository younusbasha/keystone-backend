"""
Custom Exception Classes
"""

class BaseAPIException(Exception):
    """Base exception for all API exceptions"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class ValidationException(BaseAPIException):
    """Raised when validation fails"""
    pass

class AuthenticationException(BaseAPIException):
    """Raised when authentication fails"""
    pass

class AuthorizationException(BaseAPIException):
    """Raised when authorization fails"""
    pass

class NotFoundException(BaseAPIException):
    """Raised when a resource is not found"""
    pass

class ConflictException(BaseAPIException):
    """Raised when there's a conflict (e.g., duplicate resources)"""
    pass

class InternalServerException(BaseAPIException):
    """Raised for internal server errors"""
    pass
