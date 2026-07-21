import hashlib
import secrets
from datetime import datetime, timedelta, UTC

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from src.core.exceptions import Errors
from src.config.settings import settings
import random

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

MAX_PASSWORD_BYTES = 72
REFRESH_TOKEN_BYTES = 32

# ==========================
# Password
# ==========================


def hash_password(password: str) -> str:

    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise Errors.validation_error("Password must not exceed 72 bytes")

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)


# ==========================
# Access Token (JWT)
# ==========================


def create_access_token(user_id: int) -> str:

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> int:

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise Errors.invalid_token()

        return int(user_id)

    except ExpiredSignatureError:
        raise Errors.expired_token()

    except JWTError:
        raise Errors.invalid_token()


# ==========================
# Refresh Token
# ==========================


def generate_refresh_token() -> str:

    return secrets.token_urlsafe(REFRESH_TOKEN_BYTES)


def hash_refresh_token(token: str) -> str:

    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_otp() -> str:
    """
    Generate a 6-digit One-Time Password.
    """
    return f"{random.randint(0, 999999):06d}"


def hash_otp(otp: str) -> str:
    """
    Hash OTP before storing it in database.
    """
    return hashlib.sha256(otp.encode("utf-8")).hexdigest()
