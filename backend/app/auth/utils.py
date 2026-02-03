import jwt
from ..config import settings
import bcrypt
from datetime import datetime, timedelta


def encode_jwt(
    payload: dict,
    key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.algorithm,
    expire_minutes: int = settings.access_token_expire_minutes,
    expire_days: int | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_days:
        expire = now + timedelta(days=expire_days)
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(iat=now, exp=expire)
    encoded = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.algorithm,
):
    payload = jwt.decode(token, public_key, algorithms=[algorithm])
    return payload


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
