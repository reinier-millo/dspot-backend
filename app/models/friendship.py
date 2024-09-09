from pydantic import BaseModel
from typing import List


class FriendshipBase(BaseModel):
    profile_id: int
    friend_id: int


class FriendshipConnectionResponse(BaseModel):
    path: List[int]
