from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.room_schema import (
    RoomCreateSchema,
    RoomStatusUpdateSchema,
    RoomUpdateSchema,
)
from src.services.room_service import RoomService

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("room:create"))],
)
def create_room(room_data: RoomCreateSchema):

    RoomService.create_room(room_data)

    return Responses.created(message="Room created successfully")


# ==========================
# Read
# ==========================


@router.get("", dependencies=[Depends(require_permission("room:read"))])
def get_all_rooms(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    ward_id: Optional[int] = Query(default=None),
    room_type: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
):
    return Responses.ok(
        data=RoomService.get_all_rooms(
            start_num, page_size, ward_id, room_type, status
        ),
    )


@router.get(
    "/{room_id}",
    dependencies=[Depends(require_permission("room:read"))],
)
def get_room_by_id(room_id: int):

    return Responses.ok(
        data=RoomService.get_room_by_id(room_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{room_id}",
    dependencies=[Depends(require_permission("room:update"))],
)
def update_room(room_id: int, room_data: RoomUpdateSchema):

    RoomService.update_room(room_id, room_data)

    return Responses.ok(message="Room updated successfully")


@router.put(
    "/{room_id}/status",
    dependencies=[Depends(require_permission("room:update"))],
)
def update_room_status(room_id: int, status_data: RoomStatusUpdateSchema):

    RoomService.update_room_status(room_id, status_data)

    return Responses.ok(message="Room status updated successfully")
