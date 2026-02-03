from sqlalchemy.orm import Session
from ..models.like import Like
from fastapi import HTTPException, status


class LikeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_post_id(self, post_id: int) -> list[Like]:
        db_likes = self.db.query(Like).filter(Like.post_id == post_id).all()
        return db_likes

    def add(self, post_id: int, user_id: int) -> Like:
        existing_like = (
            self.db.query(Like)
            .filter(Like.user_id == user_id, Like.post_id == post_id)
            .first()
        )

        if existing_like:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with id {user_id} already liked this post",
            )

        db_like = Like(user_id=user_id, post_id=post_id)
        self.db.add(db_like)
        self.db.commit()
        self.db.refresh(db_like)
        return db_like

    def delete(self, post_id: int, user_id: int) -> Like:
        existing_like = (
            self.db.query(Like)
            .filter(Like.user_id == user_id, Like.post_id == post_id)
            .first()
        )

        if not existing_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} do not liked this post",
            )

        self.db.delete(existing_like)
        self.db.commit()
        return existing_like
