from pydantic import BaseModel, Field
from datetime import datetime


class LikeCreate(BaseModel):
    post_id: int = Field(..., description="Post ID")
    user_id: int = Field(..., description="Like author's ID")


class LikeResponse(BaseModel):
    user_id: int
    date_created: datetime

    class Config:
        from_attributes = True


class LikeListResponse(BaseModel):
    likes: list[LikeResponse]
    total: int = Field(..., description="Total number of likes")
