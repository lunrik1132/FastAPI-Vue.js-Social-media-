from sqlalchemy.orm import Session
from typing import Optional
from ..repositories.user_repository import UserRepository
from ..schemas.user import (
    UserResponse,
    UserCreate,
    UserListResponse,
    UserUpdateBirthday,
)
from fastapi import HTTPException, status
from ..auth import utils


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_all_users(self) -> UserListResponse:
        users = self.repository.get_all()
        user_response = [UserResponse.model_validate(user) for user in users]
        return UserListResponse(users=user_response, total=len(user_response))

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        return UserResponse.model_validate(user)

    def get_user_by_login(self, user_login: int) -> UserResponse:
        user = self.repository.get_by_login(user_login)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with login {user_login} not found",
            )
        return UserResponse.model_validate(user)

    def get_all_users_by_login(self, query: str) -> UserListResponse:
        users = self.repository.get_all_by_login(query=query)
        user_response = [UserResponse.model_validate(user) for user in users]
        return UserListResponse(users=user_response, total=len(user_response))

    def create_user(self, user_data: UserCreate) -> UserResponse:
        hashed_password = utils.hash_password(user_data.password)

        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["password"] = hashed_password

        user = self.repository.create(user_dict)
        return UserResponse.model_validate(user)

    def delete_user(self, user_id: int) -> UserResponse:
        user = self.repository.delete(user_id)
        return UserResponse.model_validate(user)

    def update_user_login(self, user_id: int, new_login: str):
        user = self.repository.get_by_login(new_login)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The username {new_login} is already taken",
            )

        updated_user = self.repository.update_login(user_id, new_login)
        return UserResponse.model_validate(updated_user)

    def update_user_password(self, user_id: int, old_password: str, new_password: str):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        if not utils.validate_password(old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Old password is wrong",
            )

        hashed_password = utils.hash_password(new_password)
        updated_user = self.repository.update_password(user_id, hashed_password)
        return UserResponse.model_validate(updated_user)

    def update_user_description(self, user_id: int, new_description: Optional[str]):
        updated_user = self.repository.update_description(user_id, new_description)
        return UserResponse.model_validate(updated_user)

    def update_user_gender(self, user_id: int, new_gender: int):
        updated_user = self.repository.update_gender(user_id, new_gender)
        return UserResponse.model_validate(updated_user)

    def update_user_birthday(self, user_id: int, new_birthday: UserUpdateBirthday):
        updated_user = self.repository.update_birthday(user_id, new_birthday)
        return UserResponse.model_validate(updated_user)

    def update_user_country(self, user_id: int, new_country: str):
        updated_user = self.repository.update_country(user_id, new_country)
        return UserResponse.model_validate(updated_user)

    def update_user_url(self, user_id: int, new_url: Optional[str]):
        updated_user = self.repository.update_url(user_id, new_url)
        return UserResponse.model_validate(updated_user)
