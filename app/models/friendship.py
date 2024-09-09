from pydantic import BaseModel


class FriendshipBase(BaseModel):
    profile_id: int
    friend_id: int