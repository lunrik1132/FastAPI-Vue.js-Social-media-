from fastapi import APIRouter, Depends
from ..auth import auth
from pydantic import BaseModel
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from ..schemas.user import UserAuthSchema, UserLoginSchema


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/api/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])


@router.post("/login", response_model=TokenInfo)
def auth_user(user: UserLoginSchema = Depends(auth.validate_auth_user)):
    access_token = auth.create_access_token(user)
    refresh_token = auth.create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(
    user: UserAuthSchema = Depends(auth.get_current_auth_user_for_refresh),
):
    access_token = auth.create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/users/me")
def get_self_info(
    payload: dict = Depends(auth.get_current_token_payload_user),
    user: UserAuthSchema = Depends(auth.get_current_auth_user),
):
    iat = payload.get("iat")
    return {"login": user.login, "password": user.password, "logged_it_at": iat}
