from sqlalchemy.orm import Session
from ..repositories.chat_repository import ChatRepository
from ..repositories.user_repository import UserRepository
from ..schemas.chat import ChatResponse, ChatListResponse
from fastapi import HTTPException, status


class ChatService:
    def __init__(self, db: Session):
        self.repository = ChatRepository(db)
        self.user_repository = UserRepository(db)

    def get_chat_by_id(self, user_id: int, chat_id: int):
        if not self.repository.is_user_in_chat(user_id=user_id, chat_id=chat_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this chat",
            )

        chat = self.repository.get_by_id(chat_id=chat_id)
        return ChatResponse.model_validate(chat)

    def get_all_chats_by_user_id(
        self, user_id: int, limit: int = 6, offset: int = 0
    ) -> ChatListResponse:

        chats, total = self.repository.get_all_by_user_id(
            user_id=user_id, limit=limit, offset=offset
        )
        chats_response = []
        for chat, last_message in chats:
            data = ChatResponse.model_validate(chat)
            data.last_message = last_message
            chats_response.append(data)

        return ChatListResponse(chats=chats_response, total=total)

    def get_chat_by_two_users(
        self,
        current_user_id: int,
        other_user_id: int,
    ) -> ChatResponse:

        if not self.user_repository.get_by_id(other_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {other_user_id} not found",
            )

        chat = self.repository.get_chat_by_two_users_id(
            user1_id=current_user_id,
            user2_id=other_user_id,
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat between users not found",
            )

        return ChatResponse.model_validate(chat)

    def create_chat_by_users_ids(self, user_id, user_ids: list[int]) -> ChatResponse:
        user_ids = list(set(user_ids + [user_id]))
        for uid in user_ids:
            if not self.user_repository.get_by_id(uid):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {uid} not found",
                )

        chat = self.repository.get_chat_by_two_users_id(
            user1_id=user_ids[0], user2_id=user_ids[1]
        )
        if chat:
            return ChatResponse.model_validate(chat)

        chat = self.repository.create(user_ids=user_ids)
        return ChatResponse.model_validate(chat)

    def delete_chat_by_id(self, chat_id: int, user_id: int):
        if not self.repository.is_user_in_chat(user_id=user_id, chat_id=chat_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"You do not have permission to delete this chat",
            )

        chat = self.repository.delete(chat_id=chat_id)

        return ChatResponse.model_validate(chat)
