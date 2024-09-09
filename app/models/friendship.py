"""
Pydantic models for the friendship
"""
from typing import List
from pydantic import BaseModel


class FriendshipBase(BaseModel):
    """
    Base model for the friendship
    """
    profile_id: int
    friend_id: int


class FriendshipConnectionResponse(BaseModel):
    """
    Response model for the friendship shorter path
    """
    path: List[int]
