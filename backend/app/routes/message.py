from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.message_service import MessageService
from ..schemas.user import UserAuthSchema
from ..schemas.message import MessageCreate, MessageListResponse
from ..auth import auth

router = APIRouter(prefix="/api/chats/messages", tags=["chats/messages"])


@router.get(
    "/{chat_id}",
    response_model=MessageListResponse,
    status_code=status.HTTP_200_OK,
)
def get_chat_messages(
    chat_id: int,
    limit: int = 6,
    offset: int = 0,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
) -> MessageListResponse:
    service = MessageService(db)
    return service.get_all_messages_by_chat_id(
        user_id=user.id, chat_id=chat_id, limit=limit, offset=offset
    )


@router.post("/{chat_id}", status_code=status.HTTP_200_OK)
def send_message(
    chat_id: int,
    message_data: MessageCreate,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = MessageService(db)
    new_message = service.create_message(
        chat_id=chat_id, text=message_data.text, user_id=user.id
    )
    return {"message": "Comment added", "new_comment": new_message}
