"""
Pydantic models for the health validation
"""
from pydantic import BaseModel


class Health(BaseModel):
    """
    Health model
    """
    status: str = "ok"
    version: str
