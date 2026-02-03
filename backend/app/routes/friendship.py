from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.friendship_service import FriendshipService
from ..schemas.user import UserAuthSchema
from ..schemas.friendship import FriendshipCreate, FriendshipListResponse
from ..auth import auth

router = APIRouter(prefix="/api/users/friends", tags=["users/friends"])


@router.get(
    "/status/{user_id}",
    status_code=status.HTTP_200_OK,
)
def check_friendship_status(
    user_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = FriendshipService(db)
    status = service.check_friendship_between_two_users(
        user1_id=user.id, user2_id=user_id
    )
    return {
        "status": status["status"],
        "id": status["id"],
        "requester_id": status["requester_id"],
    }


@router.get(
    "/accepted/{user_id}",
    response_model=FriendshipListResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_friends(
    user_id: int, limit: int = 6, offset: int = 0, db: Session = Depends(get_db)
) -> FriendshipListResponse:
    service = FriendshipService(db)
    return service.get_all_friends_by_user_id(
        user_id=user_id, limit=limit, offset=offset
    )


@router.delete(
    "/accepted/{friendship_id}",
    status_code=status.HTTP_200_OK,
)
def delete_friend(
    friendship_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = FriendshipService(db)
    deleted_friendship = service.delete_friendship(
        user_id=user.id, friendship_id=friendship_id
    )
    return deleted_friendship


@router.get(
    "/pending", response_model=FriendshipListResponse, status_code=status.HTTP_200_OK
)
def get_user_pending_requests(
    limit: int = 6,
    offset: int = 0,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
) -> FriendshipListResponse:
    service = FriendshipService(db)
    return service.get_pending_requests_by_user_id(
        user_id=user.id, limit=limit, offset=offset
    )


@router.post("/requests/send", status_code=status.HTTP_200_OK)
def send_friend_request(
    friendship_data: FriendshipCreate,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = FriendshipService(db)
    new_friendship = service.send_friend_request(
        requester_id=user.id, addressee_id=friendship_data.addressee_id
    )
    return new_friendship


@router.delete(
    "/requests/reject/{requester_id}",
    status_code=status.HTTP_200_OK,
)
def reject_friend_request(
    requester_id: int,
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
    db: Session = Depends(get_db),
):
    service = FriendshipService(db)
    deleted_friendship = service.reject_friend_request(
        requester_id=requester_id, addressee_id=user.id
    )
    return deleted_friendship
