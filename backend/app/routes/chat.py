from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.chat_service import ChatService
from ..schemas.user import UserAuthSchema
from ..schemas.chat import ChatCreate, ChatListResponse, ChatResponse
from ..auth import auth

router = APIRouter(prefix="/api/chats", tags=["chats"])


@router.get(
    "",
    response_model=ChatListResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_chats(
    limit: int = 6,
    offset: int = 0,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
) -> ChatListResponse:
    service = ChatService(db)
    return service.get_all_chats_by_user_id(user_id=user.id, limit=limit, offset=offset)


@router.get(
    "/{chat_id}",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def get_chat_by_id(
    chat_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
) -> ChatListResponse:
    service = ChatService(db)
    return service.get_chat_by_id(user_id=user.id, chat_id=chat_id)


@router.get(
    "/user/{user_id}",
    response_model=ChatListResponse,
    status_code=status.HTTP_200_OK,
)
def get_chat_with_user(
    user_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
) -> ChatListResponse:
    service = ChatService(db)
    return service.get_chat_by_two_users(
        current_user_id=user.id,
        other_user_id=user_id,
    )


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def create_chat(
    chat_data: ChatCreate,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
) -> ChatResponse:
    service = ChatService(db)
    return service.create_chat_by_users_ids(
        user_id=user.id, user_ids=chat_data.user_ids
    )


@router.delete("/{chat_id}", status_code=status.HTTP_200_OK)
def delete_chat_by_id(
    chat_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    deleted_post = service.delete_chat_by_id(chat_id=chat_id, user_id=user.id)
    return {"message": "Post deleted", "deleted_post": deleted_post}
