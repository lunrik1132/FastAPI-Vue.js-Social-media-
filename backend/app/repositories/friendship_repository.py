from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from ..models.friendship import Friendship


class FriendshipRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, friendship_id: int):
        return (
            self.db.query(Friendship)
            .options(
                joinedload(Friendship.requester),
                joinedload(Friendship.addressee),
            )
            .filter_by(id=friendship_id)
            .first()
        )

    def get_all_by_user_id(self, user_id: int, limit: int = 6, offset: int = 0):
        base_query = self.db.query(Friendship).filter(
            Friendship.status == "accepted",
            or_(
                Friendship.requester_id == user_id,
                Friendship.addressee_id == user_id,
            ),
        )
        total = base_query.count()

        friends = (
            base_query.options(
                joinedload(Friendship.requester),
                joinedload(Friendship.addressee),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        return friends, total

    def get_pending_by_user_id(
        self,
        user_id: int,
        limit: int = 6,
        offset: int = 0,
    ):

        base_query = self.db.query(Friendship).filter(
            Friendship.addressee_id == user_id,
            Friendship.status == "pending",
        )

        total = base_query.count()

        friends = (
            base_query.options(
                joinedload(Friendship.requester),
                joinedload(Friendship.addressee),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        return friends, total

    def get_between_users(self, user1_id: int, user2_id: int):
        return (
            self.db.query(Friendship)
            .filter(
                or_(
                    and_(
                        Friendship.requester_id == user1_id,
                        Friendship.addressee_id == user2_id,
                    ),
                    and_(
                        Friendship.requester_id == user2_id,
                        Friendship.addressee_id == user1_id,
                    ),
                )
            )
            .first()
        )

    def save(self, friendship: Friendship):
        self.db.commit()
        self.db.refresh(friendship)

    def create(self, requester_id: int, addressee_id: int):
        friendship = Friendship(
            requester_id=requester_id,
            addressee_id=addressee_id,
            status="pending",
        )
        self.db.add(friendship)
        self.db.commit()
        self.db.refresh(friendship)
        return friendship

    def delete(self, friendship: Friendship):
        self.db.delete(friendship)
        self.db.commit()
        return {"detail": "Friendship deleted"}
