from pydantic import BaseModel, Field
from datetime import datetime
from .user import UserShortResponse


class CommentCreate(BaseModel):
    text: str = Field(..., description="Comment text", max_length=150, min_length=1)


class CommentResponse(BaseModel):
    id: int
    author_id: int
    text: str
    author: UserShortResponse = Field(..., description="Comment's author details")
    date_created: datetime

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]
    total: int = Field(..., description="Total number of comments")
