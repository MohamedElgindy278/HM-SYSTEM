from fastapi import APIRouter, Depends, Request

from src.core.deps import get_current_user
from src.core.responses import Responses
from src.schemas.auth_schema import (
    ChangePasswordSchema,
    CurrentUserSchema,
    LoginSchema,
    RefreshTokenSchema,
)
from src.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# ==========================
# Login
# ==========================


@router.post("/login")
def login(login_data: LoginSchema, request: Request):

    ip_address = request.client.host if request.client else None

    return Responses.ok(
        data=AuthService.login(login_data, ip_address),
    )


# ==========================
# Refresh
# ==========================


@router.post("/refresh")
def refresh(refresh_data: RefreshTokenSchema):

    return Responses.ok(
        data=AuthService.refresh(refresh_data),
    )


# ==========================
# Logout
# ==========================


@router.post("/logout")
def logout(refresh_data: RefreshTokenSchema):

    AuthService.logout(refresh_data)

    return Responses.ok(message="Logged out successfully")


# ==========================
# Change Password
# ==========================


@router.post("/change-password")
def change_password(
    data: ChangePasswordSchema,
    current_user: CurrentUserSchema = Depends(get_current_user),
):

    AuthService.change_password(current_user.user_id, data)

    return Responses.ok(message="Password changed successfully")


# ==========================
# Current User
# ==========================


@router.get("/me")
def get_me(current_user: CurrentUserSchema = Depends(get_current_user)):

    return Responses.ok(data=current_user)
