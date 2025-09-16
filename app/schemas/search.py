"""
Search Schemas
"""
from typing import List, Dict, Any
from pydantic import BaseModel

class SearchResponse(BaseModel):
    """Search response schema"""
    results: List[Dict[str, Any]] = []
    total: int = 0
    query: str
    filters: Dict[str, Any] = {}

class GlobalSearchResponse(BaseModel):
    """Global search response schema"""
    projects: List[Dict[str, Any]] = []
    requirements: List[Dict[str, Any]] = []
    tasks: List[Dict[str, Any]] = []
    agents: List[Dict[str, Any]] = []
    total: int = 0
    query: str
