from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.domains.auth.config import auth_settings
from src.domains.auth.exceptions import InvalidToken


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=auth_settings.access_token_expire_minutes
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, auth_settings.jwt_secret, algorithm=auth_settings.jwt_algorithm)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token, auth_settings.jwt_secret, algorithms=[auth_settings.jwt_algorithm]
        )
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise InvalidToken()
