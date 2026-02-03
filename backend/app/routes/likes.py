from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.like_service import LikeService
from ..schemas.user import UserAuthSchema
from ..auth import auth

router = APIRouter(prefix="/api/posts", tags=["posts/likes"])


@router.get("/{post_id}/likes")
def get_likes_by_post_id(post_id: int, db: Session = Depends(get_db)):
    service = LikeService(db)
    likes = service.get_all_likes_by_post_id(post_id)
    return likes


@router.post("/{post_id}/likes")
def add_like(
    post_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = LikeService(db)
    like = service.add_like(post_id, user.id)
    return {"message": "Post liked", "like_data": like}


@router.delete("/{post_id}/likes")
def delete_like(
    post_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = LikeService(db)
    like = service.delete_like(post_id, user.id)
    return {"message": "Post unliked", "like_data": like}
