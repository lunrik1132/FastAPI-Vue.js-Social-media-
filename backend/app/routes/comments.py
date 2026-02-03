from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.comment_service import CommentService
from ..schemas.comment import CommentCreate, CommentListResponse, CommentResponse
from ..schemas.user import UserAuthSchema
from ..auth import auth

router = APIRouter(prefix="/api/posts", tags=["posts/comments"])


@router.get(
    "/{post_id}/comments",
    response_model=CommentListResponse,
    status_code=status.HTTP_200_OK,
)
def get_comments_by_post_id(
    post_id: int, limit: int = 3, offset: int = 1, db: Session = Depends(get_db)
):
    service = CommentService(db)
    comments = service.get_all_comments_by_post_id(post_id, limit, offset)
    return comments


@router.get(
    "/{post_id}/comments/{comment_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_200_OK,
)
def get_comment_by_id(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    service = CommentService(db)
    comments = service.get_comment_by_id(post_id, comment_id)
    return comments


@router.post("/{post_id}/comments", status_code=status.HTTP_200_OK)
def add_comment(
    post_id: int,
    comment_data: CommentCreate,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = CommentService(db)
    new_comment = service.add_comment(
        post_id=post_id, text=comment_data.text, author_id=user.id
    )
    return {"message": "Comment added", "new_comment": new_comment}


@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment_by_id(
    post_id: int,
    comment_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = CommentService(db)
    deleted_comment = service.delete_comment_by_id(
        post_id=post_id, comment_id=comment_id, user_id=user.id
    )
    return {"message": "Comment deleted", "deleted_comment": deleted_comment}
