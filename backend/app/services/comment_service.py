from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..repositories.post_repository import PostRepository
from ..repositories.comment_repository import CommentRepository
from ..schemas.comment import CommentResponse, CommentListResponse
from fastapi import HTTPException, status


class CommentService:
    def __init__(self, db: Session):
        self.post_repository = PostRepository(db)
        self.user_repository = UserRepository(db)
        self.comment_repository = CommentRepository(db)

    def get_all_comments_by_post_id(
        self, post_id: int, limit: int = 3, offset: int = 1
    ) -> CommentListResponse:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )
        comments = self.comment_repository.get_all_by_post_id(post_id, limit, offset)
        comments_response = [
            CommentResponse.model_validate(comment) for comment in comments
        ]
        return CommentListResponse(
            comments=comments_response, total=len(comments_response)
        )

    def get_comment_by_id(self, comment_id: int) -> CommentResponse:
        comment = self.comment_repository.get_by_id(comment_id)

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id {comment_id} not found",
            )

        return CommentResponse.model_validate(comment)

    def add_comment(self, post_id: int, text: str, author_id: int) -> CommentResponse:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )

        comment = self.comment_repository.add(
            post_id=post_id, text=text, author_id=author_id
        )
        return CommentResponse.model_validate(comment)

    def delete_comment_by_id(
        self, post_id: int, comment_id: int, user_id: int
    ) -> CommentResponse:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id {comment_id} not found",
            )

        if comment.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"You do not have permission to delete this comment",
            )

        comment = self.comment_repository.delete_by_comment_id(comment_id)
        return CommentResponse.model_validate(comment)
