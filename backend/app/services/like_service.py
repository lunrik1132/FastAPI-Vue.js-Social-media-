from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..repositories.post_repository import PostRepository
from ..repositories.like_repository import LikeRepository
from ..schemas.like import LikeResponse, LikeListResponse
from fastapi import HTTPException, status


class LikeService:
    def __init__(self, db: Session):
        self.post_repository = PostRepository(db)
        self.user_repository = UserRepository(db)
        self.like_repository = LikeRepository(db)

    def get_all_likes_by_post_id(self, post_id: int) -> LikeListResponse:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )
        likes = self.like_repository.get_all_by_post_id(post_id)
        likes_response = [LikeResponse.model_validate(like) for like in likes]
        return LikeListResponse(likes=likes_response, total=len(likes_response))

    def add_like(self, post_id: int, user_id: int) -> LikeResponse:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )

        like = self.like_repository.add(post_id, user_id)
        return LikeResponse.model_validate(like)

    def delete_like(self, post_id: int, user_id: int) -> LikeResponse:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )

        like = self.like_repository.delete(post_id, user_id)
        return LikeResponse.model_validate(like)
