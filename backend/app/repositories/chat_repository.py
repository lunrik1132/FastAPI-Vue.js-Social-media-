from sqlalchemy.orm import Session, joinedload, selectinload, aliased
from sqlalchemy import func, select
from ..models.chat import Chat, ChatMember
from ..models.message import Message
from fastapi import HTTPException, status


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, chat_id: int):
        return (
            self.db.query(Chat)
            .options(selectinload(Chat.members).selectinload(ChatMember.user))
            .filter(Chat.id == chat_id)
            .first()
        )

    def get_all_by_user_id(self, user_id: int, limit: int = 6, offset: int = 0):
        last_message_subq = (
            self.db.query(
                Message.chat_id.label("chat_id"),
                func.max(Message.date_created).label("last_date"),
            )
            .group_by(Message.chat_id)
            .subquery()
        )

        last_message = aliased(Message)
        base_query = (
            self.db.query(Chat, last_message.text.label("last_message"))
            .join(Chat.members)
            .outerjoin(
                last_message_subq,
                last_message_subq.c.chat_id == Chat.id,
            )
            .outerjoin(
                last_message,
                (last_message.chat_id == Chat.id)
                & (last_message.date_created == last_message_subq.c.last_date),
            )
            .filter(ChatMember.user_id == user_id)
        )
        total = base_query.count()

        chats = (
            base_query.options(selectinload(Chat.members).selectinload(ChatMember.user))
            .order_by(last_message_subq.c.last_date.desc().nullslast())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return chats, total

    def get_chat_by_two_users_id(self, user1_id: int, user2_id: int):
        chat_id_select = (
            select(ChatMember.chat_id)
            .where(ChatMember.user_id.in_([user1_id, user2_id]))
            .group_by(ChatMember.chat_id)
            .having(func.count(func.distinct(ChatMember.user_id)) == 2)
        )

        return (
            self.db.query(Chat)
            .filter(Chat.id.in_(chat_id_select))
            .options(selectinload(Chat.members).selectinload(ChatMember.user))
            .first()
        )

    def is_user_in_chat(self, user_id: int, chat_id: int):
        return (
            self.db.query(ChatMember.id)
            .filter(ChatMember.chat_id == chat_id, ChatMember.user_id == user_id)
            .first()
        )

    def create(self, user_ids: list[int]):
        db_chat = Chat()
        self.db.add(db_chat)
        self.db.flush()
        db_chat.members = [ChatMember(user_id=uid) for uid in user_ids]
        self.db.commit()
        self.db.refresh(db_chat)

        db_chat = (
            self.db.query(Chat)
            .options(joinedload(Chat.members).joinedload(ChatMember.user))
            .filter_by(id=db_chat.id)
            .first()
        )
        return db_chat

    def delete(self, chat_id: int):
        db_chat = (
            self.db.query(Chat)
            .options(selectinload(Chat.members).selectinload(ChatMember.user))
            .filter(Chat.id == chat_id)
            .first()
        )

        if not db_chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chat with id {chat_id} does not exist",
            )

        self.db.delete(db_chat)
        self.db.commit()
        return db_chat
