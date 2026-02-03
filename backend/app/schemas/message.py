from pydantic import BaseModel, Field
from datetime import datetime
from .user import UserShortResponse


class MessageCreate(BaseModel):
    text: str = Field(..., description="Comment text", max_length=1000, min_length=1)


class MessageResponse(BaseModel):
    id: int
    text: str
    sender_id: int
    sender: UserShortResponse
    date_created: datetime

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: list[MessageResponse]
    total: int = Field(..., description="Total number of messages")
