from fastapi import Depends, HTTPException, status
from ..schemas.user import UserAuthSchema, UserLoginSchema
from .utils import *
from jwt.exceptions import InvalidTokenError
from ..config import settings
from fastapi.security import (
    OAuth2PasswordBearer,
)
from ..services.user_service import UserService
from ..database import get_db
from sqlalchemy.orm import Session

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/jwt/login/")


def validate_auth_user(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password"
    )

    service = UserService(db)
    user = service.get_user_by_login(user_data.login)
    if not user:
        raise unauthed_exc

    if not validate_password(
        password=user_data.password, hashed_password=user.password
    ):
        raise unauthed_exc
    return UserAuthSchema.model_validate(user.model_dump())


def get_current_token_payload_user(
    token: str = Depends(oauth2_scheme),
) -> UserAuthSchema:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token error: {e}"
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload_user),
    db: Session = Depends(get_db),
) -> UserAuthSchema:
    token_type = payload.get("type")
    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: {token_type}",
        )
    id: str = payload.get("id")
    service = UserService(db)
    user = service.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid(User not found)",
        )
    return UserAuthSchema.model_validate(user.model_dump())


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload_user),
    db: Session = Depends(get_db),
) -> UserAuthSchema:
    token_type = payload.get("type")
    if token_type != REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: {token_type}",
        )
    id: str = payload.get("id")
    service = UserService(db)
    user = service.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid(User not found)",
        )
    return UserAuthSchema.model_validate(user.model_dump())


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes=settings.access_token_expire_minutes,
    expire_days: int | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    token = encode_jwt(
        payload=jwt_payload, expire_minutes=expire_minutes, expire_days=expire_days
    )
    return token


def create_access_token(user: UserAuthSchema) -> str:
    jwt_payload = {"sub": user.login, "id": user.id, "username": user.login}
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.access_token_expire_minutes,
    )


def create_refresh_token(user: UserAuthSchema) -> str:
    jwt_payload = {"sub": user.login, "id": user.id}

    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_days=settings.refresh_token_expire_days,
    )
