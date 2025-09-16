"""
Base Model Class
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, String
from sqlalchemy.ext.declarative import declared_attr
import uuid

from app.config.database import Base

class BaseModel(Base):
    """Base model class with common fields"""
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
