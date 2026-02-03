from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.user import User
from ..schemas.user import UserUpdateBirthday
from fastapi import HTTPException, status


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_login(self, user_login: str) -> Optional[User]:
        return self.db.query(User).filter(User.login == user_login).first()

    def get_all_by_login(self, query: str, limit: int = 10) -> List[User]:
        return (
            self.db.query(User)
            .filter(
                User.login.ilike(f"%{query}%")
            )  # поиск по подстроке, регистронезависимый
            .limit(limit)
            .all()
        )

    def create(self, user_data: dict) -> User:
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        self.db.delete(db_user)
        self.db.commit()
        return db_user

    def update_login(self, user_id: int, new_login: str):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        db_user.login = new_login
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_password(self, user_id: int, hashed_password: bytes):
        db_user = self.db.query(User).filter(User.id == user_id).first()

        db_user.password = hashed_password
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_description(self, user_id: int, new_description: Optional[str]):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        db_user.description = new_description
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_gender(self, user_id: int, new_gender: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        db_user.gender = new_gender
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_birthday(self, user_id: int, new_birthday: UserUpdateBirthday):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        db_user.birthday = new_birthday.new_birthday
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_country(self, user_id: int, new_country: str):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        db_user.country = new_country
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_url(self, user_id: int, new_url: Optional[str]):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        db_user.image_url = new_url
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
