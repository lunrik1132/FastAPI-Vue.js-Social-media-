from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from ..models.post import Post
from ..models.like import Like
from ..models.comment import Comment
from fastapi import HTTPException, status


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, limit: int = 3, offset: int = 0):
        return (
            self.db.query(Post, func.count(Comment.id).label("comments_count"))
            .outerjoin(Comment, Comment.post_id == Post.id)
            .options(
                joinedload(Post.author),
                joinedload(Post.destination),
                joinedload(Post.likes).joinedload(Like.user),
            )
            .group_by(Post.id)
            .order_by(Post.date_created.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_by_id(self, post_id: int) -> Optional[Post]:
        return (
            self.db.query(Post)
            .options(
                joinedload(Post.author),
                joinedload(Post.destination),
                joinedload(Post.likes).joinedload(Like.user),
                joinedload(Post.comments).joinedload(Comment.author),
            )
            .filter(Post.id == post_id)
            .first()
        )

    def get_all_by_author_id(self, author_id: int, limit: int = 3, offset: int = 0):
        return (
            self.db.query(Post, func.count(Comment.id).label("comments_count"))
            .outerjoin(Comment, Comment.post_id == Post.id)
            .options(
                joinedload(Post.author),
                joinedload(Post.destination),
                joinedload(Post.likes).joinedload(Like.user),
            )
            .filter(Post.author_id == author_id)
            .order_by(Post.date_created.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_all_by_destination_id(
        self, destination_id: int, limit: int = 3, offset: int = 0
    ):
        return (
            self.db.query(Post, func.count(Comment.id).label("comments_count"))
            .outerjoin(Comment, Comment.post_id == Post.id)
            .options(
                joinedload(Post.author),
                joinedload(Post.destination),
                joinedload(Post.likes).joinedload(Like.user),
            )
            .filter(Post.destination_id == destination_id)
            .group_by(Post.id)
            .order_by(Post.date_created.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create(self, author_id: int, text: str, destination_id: int) -> Post:
        db_post = Post(author_id=author_id, destination_id=destination_id, text=text)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

    def delete_by_id(self, post_id: int) -> Post:
        db_post = self.db.query(Post).filter(Post.id == post_id).first()
        self.db.delete(db_post)
        self.db.commit()
        return db_post

    def delete_by_author_id(self, author_id: int) -> List[Post]:
        db_posts = (
            self.db.query(Post)
            .options(
                joinedload(Post.author),
                joinedload(Post.destination),
                joinedload(Post.likes).joinedload(Like.user),
                joinedload(Post.comments).joinedload(Comment.author),
            )
            .filter(Post.author_id == author_id)
            .all()
        )
        if not db_posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {author_id} do not have posts",
            )

        for post in db_posts:
            self.db.delete(post)
            self.db.commit()
        return db_posts

    def update_text(self, post_id: int, new_text: str):
        db_post = (
            self.db.query(Post)
            .options(
                joinedload(Post.author),
                joinedload(Post.destination),
                joinedload(Post.likes).joinedload(Like.user),
                joinedload(Post.comments).joinedload(Comment.author),
            )
            .filter(Post.id == post_id)
            .first()
        )
        if not db_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} do not have posts",
            )

        db_post.text = new_text
        self.db.commit()
        self.db.refresh(db_post)
        return db_post
