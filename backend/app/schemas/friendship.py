from pydantic import BaseModel, Field
from .user import UserShortResponse
from enum import Enum


class FriendshipBase(BaseModel):
    addressee_id: int = Field(..., description="User's ID who receive proposition")


class FriendshipCreate(FriendshipBase):
    pass


class FriendshipStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    blocked = "blocked"


class FriendshipResponse(BaseModel):
    id: int
    requester_id: int
    addressee_id: int
    status: FriendshipStatus
    requester: UserShortResponse
    addressee: UserShortResponse

    class Config:
        from_attributes = True


class FriendshipListResponse(BaseModel):
    friends: list[FriendshipResponse]
    total: int = Field(..., description="Total number of friends")
