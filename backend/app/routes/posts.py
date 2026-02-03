from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.post_service import PostService
from ..schemas.post import PostListResponse, PostCreate, PostResponse, PostUpdate
from ..schemas.user import UserAuthSchema
from ..auth import auth

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=PostListResponse, status_code=status.HTTP_200_OK)
def get_posts(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    service = PostService(db)
    return service.get_all_posts(limit=limit, offset=offset)


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Session = Depends(get_db)):
    service = PostService(db)
    return service.get_post_by_id(post_id)


@router.get(
    "/user/author/{author_id}",
    response_model=PostListResponse,
    status_code=status.HTTP_200_OK,
)
def get_posts_by_author_id(
    author_id: int, limit: int = 3, offset: int = 0, db: Session = Depends(get_db)
):
    service = PostService(db)
    return service.get_all_posts_by_author_id(author_id, limit, offset)


@router.get(
    "/user/destination/{destination_id}",
    response_model=PostListResponse,
    status_code=status.HTTP_200_OK,
)
def get_posts_by_destination_id(
    destination_id: int, limit: int = 3, offset: int = 0, db: Session = Depends(get_db)
):
    service = PostService(db)
    return service.get_all_posts_by_destination_id(destination_id, limit, offset)


@router.post("", status_code=status.HTTP_200_OK)
def add_post(
    post_data: PostCreate,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = PostService(db)
    new_post = service.create_post(
        author_id=user.id,
        destination_id=post_data.destination_id,
        text=post_data.text,
    )
    return {"message": "Post added", "new_post": new_post}


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post_by_id(
    post_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = PostService(db)
    deleted_post = service.delete_post_by_id(post_id=post_id, user_id=user.id)
    return {"message": "Post deleted", "deleted_post": deleted_post}


@router.delete("/user/{author_id}", status_code=status.HTTP_200_OK)
def delete_posts_by_author_id(author_id: int, db: Session = Depends(get_db)):
    service = PostService(db)
    deleted_posts = service.delete_posts_by_author_id(author_id)
    return {"message": "Posts deleted", "deleted_posts": deleted_posts}


@router.patch("/{post_id}", status_code=status.HTTP_200_OK)
def update_post_text(
    post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)
):
    service = PostService(db)
    updated_post = service.update_post_text(post_id, post_data.text)
    return {"message": "Post updated", "updated_post": updated_post}
