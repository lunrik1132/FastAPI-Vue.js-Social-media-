from sqlalchemy.orm import Session
from ..repositories.friendship_repository import FriendshipRepository
from ..repositories.user_repository import UserRepository
from ..schemas.friendship import FriendshipResponse, FriendshipListResponse
from fastapi import HTTPException, status
from datetime import datetime


class FriendshipService:
    def __init__(self, db: Session):
        self.repository = FriendshipRepository(db)
        self.user_repository = UserRepository(db)

    def check_friendship_between_two_users(self, user1_id: int, user2_id: int):
        friendship = self.repository.get_between_users(user1_id, user2_id)

        if not friendship:
            return {"status": "rejected", "id": None, "requester_id": None}

        return {
            "status": friendship.status,
            "id": friendship.id,
            "requester_id": friendship.requester_id,
        }

    def get_all_friends_by_user_id(
        self, user_id: int, limit: int = 6, offset: int = 0
    ) -> FriendshipListResponse:
        friends_request = self.repository.get_all_by_user_id(
            user_id=user_id, limit=limit, offset=offset
        )
        friends, total = friends_request
        friends_response = [
            FriendshipResponse.model_validate(friend) for friend in friends
        ]
        return FriendshipListResponse(friends=friends_response, total=total)

    def get_pending_requests_by_user_id(
        self,
        user_id: int,
        limit: int = 6,
        offset: int = 0,
    ) -> FriendshipListResponse:
        friends_request = self.repository.get_pending_by_user_id(
            user_id=user_id, limit=limit, offset=offset
        )
        friends, total = friends_request
        friends_response = [
            FriendshipResponse.model_validate(friend) for friend in friends
        ]
        return FriendshipListResponse(friends=friends_response, total=total)

    def send_friend_request(self, requester_id: int, addressee_id: int):
        if requester_id == addressee_id:
            raise HTTPException(400, "You cannot add yourself as a friend")

        if not self.user_repository.get_by_id(addressee_id):
            raise HTTPException(404, f"User with id {addressee_id} not found")

        existing = self.repository.get_between_users(requester_id, addressee_id)
        if existing:
            if (
                existing.status == "pending"
                and existing.requester_id == addressee_id
                and existing.addressee_id == requester_id
            ):
                existing.status = "accepted"
                existing.accepted_at = datetime.utcnow()
                self.repository.save(existing)
                return existing

            raise HTTPException(400, "Friend request already exists")

        friendship = self.repository.create(
            requester_id=requester_id,
            addressee_id=addressee_id,
        )

        return friendship

    def reject_friend_request(self, requester_id: int, addressee_id: int):
        if requester_id == addressee_id:
            raise HTTPException(400, "You cannot reject yourself")

        friendship = self.repository.get_between_users(requester_id, addressee_id)

        if not friendship:
            raise HTTPException(404, f"Friend request not found")

        if friendship.status != "pending":
            raise HTTPException(400, "Friend request is not pending")

        if friendship.addressee_id != addressee_id:
            raise HTTPException(403, "You cannot reject this request")

        return self.repository.delete(friendship)

    def delete_friendship(self, user_id: int, friendship_id: int):
        friendship = self.repository.get_by_id(friendship_id=friendship_id)

        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This friendship do not found",
            )

        if user_id != friendship.addressee_id and user_id != friendship.requester_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You do not have permission to delete this friendship",
            )

        return self.repository.delete(friendship)
