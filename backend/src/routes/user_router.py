from fastapi import APIRouter

from src.core.responses import Responses
from src.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from src.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# ==========================
# Create
# ==========================


@router.post("/")
def create_user(user_data: UserCreateSchema):

    UserService.create_user(user_data)

    return Responses.ok(
        message="User created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("/")
def get_all_users():

    return Responses.ok(
        data=UserService.get_all_users(),
    )


@router.get("/{user_id}")
def get_user_by_id(user_id: int):

    return Responses.ok(
        data=UserService.get_user_by_id(user_id),
    )


# ==========================
# Update
# ==========================


@router.put("/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
):

    UserService.update_user(
        user_id,
        user_data,
    )

    return Responses.ok(
        message="User updated successfully",
    )


# ==========================
# Delete
# ==========================


@router.delete("/{user_id}")
def delete_user(user_id: int):

    UserService.delete_user(user_id)

    return Responses.ok(
        message="User deleted successfully",
    )
