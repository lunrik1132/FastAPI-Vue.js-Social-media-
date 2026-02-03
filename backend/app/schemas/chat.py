from pydantic import BaseModel, Field
from datetime import datetime
from .user import UserShortResponse


class ChatCreate(BaseModel):
    user_ids: list[int] = Field(..., min_length=1)


class ChatMemberResponse(BaseModel):
    user_id: int
    user: UserShortResponse

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    id: int
    members: list[ChatMemberResponse]
    last_message: str | None = None
    date_created: datetime

    class Config:
        from_attributes = True


class ChatListResponse(BaseModel):
    chats: list[ChatResponse]
    total: int = Field(..., description="Total number of chats")
