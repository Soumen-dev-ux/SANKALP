from datetime import datetime, timedelta, timezone

import jwt
import bcrypt
from app.core.config import settings



def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    pwd_bytes = plain_password.encode("utf-8")[:72]
    hash_bytes = password_hash.encode("utf-8")
    try:
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False



def create_access_token(
    user_id: int,
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )