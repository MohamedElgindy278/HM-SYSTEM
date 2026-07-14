from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
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


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("user:create"))],
)
def create_user(user_data: UserCreateSchema):

    UserService.create_user(user_data)

    return Responses.created(message="User created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("user:read"))],
)
def get_all_users(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):

    return Responses.ok(
        data=UserService.get_all_users(start_num, page_size),
    )


@router.get(
    "/{user_id}",
    dependencies=[Depends(require_permission("user:read"))],
)
def get_user_by_id(user_id: int):

    return Responses.ok(
        data=UserService.get_user_by_id(user_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{user_id}",
    dependencies=[Depends(require_permission("user:update"))],
)
def update_user(user_id: int, user_data: UserUpdateSchema):

    UserService.update_user(user_id, user_data)

    return Responses.ok(message="User updated successfully")


# ==========================
# Delete
# ==========================


@router.delete(
    "/{user_id}",
    dependencies=[Depends(require_permission("user:delete"))],
)
def delete_user(user_id: int):

    UserService.delete_user(user_id)

    return Responses.deleted(message="User deleted successfully")
