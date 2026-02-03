from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .user import UserShortResponse
from .like import LikeResponse


class PostBase(BaseModel):
    destination_id: int = Field(..., description="User's ID who receive post")
    text: str = Field(..., min_length=1, max_length=200, description="Post's text")


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    text: str = Field(..., min_length=1, max_length=200, description="Post's text")


class PostResponse(BaseModel):
    id: int = Field(..., description="Unique post's id")
    text: str
    date_created: datetime
    author_id: int
    destination_id: int

    author: UserShortResponse = Field(..., description="Post's author details")
    destination: UserShortResponse = Field(
        ..., description="User, who receive post, details"
    )
    likes: Optional[list[LikeResponse]] = []
    comments_count: Optional[int] = 0

    class Config:
        from_attributes = True


class PostDeleted(BaseModel):
    id: int = Field(..., description="Unique post's id")
    text: str
    date_created: datetime
    author_id: int
    destination_id: int

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    posts: list[PostResponse]
    total: int = Field(..., description="Total number of posts")
