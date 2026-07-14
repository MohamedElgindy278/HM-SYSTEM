from typing import List

from pydantic import BaseModel, Field

# ==========================
# Login
# ==========================


class LoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=1, max_length=72)


# ==========================
# Tokens
# ==========================


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenSchema(BaseModel):
    refresh_token: str


# ==========================
# Current User
# ==========================


class CurrentUserSchema(BaseModel):
    user_id: int
    username: str
    is_active: bool
    roles: List[str] = []
    permissions: List[str] = []


# ==========================
# Change Password
# ==========================


class ChangePasswordSchema(BaseModel):
    old_password: str = Field(..., min_length=1, max_length=72)
    new_password: str = Field(..., min_length=8, max_length=72)
