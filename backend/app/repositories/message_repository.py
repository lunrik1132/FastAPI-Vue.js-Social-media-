from sqlalchemy.orm import Session, joinedload, selectinload
from ..models.message import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, chat_id: int):
        return (
            self.db.query(Message)
            .options(
                joinedload(Message.chat),
                joinedload(Message.sender),
            )
            .filter_by(id=chat_id)
            .first()
        )

    def get_all_by_chat_id(self, chat_id: int, limit: int = 6, offset: int = 0):
        base_query = self.db.query(Message).filter(Message.chat_id == chat_id)
        total = base_query.count()

        messages = (
            base_query.options(selectinload(Message.sender))
            .order_by(Message.date_created.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return list(reversed(messages)), total

    def create(self, chat_id: int, user_id: int, text: str):
        message = Message(chat_id=chat_id, sender_id=user_id, text=text)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
