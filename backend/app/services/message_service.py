from sqlalchemy.orm import Session
from ..repositories.message_repository import MessageRepository
from ..repositories.chat_repository import ChatRepository
from ..schemas.message import MessageResponse, MessageListResponse
from fastapi import HTTPException, status


class MessageService:
    def __init__(self, db: Session):
        self.repository = MessageRepository(db)
        self.chat_repository = ChatRepository(db)

    def get_all_messages_by_chat_id(
        self, user_id: int, chat_id: int, limit: int = 6, offset: int = 0
    ) -> MessageListResponse:
        if not self.chat_repository.is_user_in_chat(user_id=user_id, chat_id=chat_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this chat",
            )

        messages_request = self.repository.get_all_by_chat_id(
            chat_id=chat_id, limit=limit, offset=offset
        )
        messages, total = messages_request
        messages_response = [
            MessageResponse.model_validate(message) for message in messages
        ]
        return MessageListResponse(messages=messages_response, total=total)

    def create_message(self, chat_id: int, text: str, user_id: int):
        if not self.chat_repository.is_user_in_chat(user_id=user_id, chat_id=chat_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this chat",
            )

        message = self.repository.create(chat_id=chat_id, user_id=user_id, text=text)
        return MessageResponse.model_validate(message)
