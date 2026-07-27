from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

RoomType = Literal[
    "Operation", "Delivery", "Isolation", "Procedure", "Consultation", "Patient"
]
RoomStatus = Literal["Available", "Occupied", "Maintenance", "Reserved"]


class RoomCreateSchema(BaseModel):
    ward_id: int = Field(..., gt=0)
    room_number: str = Field(..., min_length=1, max_length=20)
    room_type: RoomType
    status: RoomStatus = "Available"
    floor_number: Optional[int] = Field(default=None, ge=0)


class RoomUpdateSchema(BaseModel):
    ward_id: Optional[int] = Field(default=None, gt=0)
    room_number: Optional[str] = Field(default=None, min_length=1, max_length=20)
    room_type: Optional[RoomType] = None
    floor_number: Optional[int] = Field(default=None, ge=0)


class RoomStatusUpdateSchema(BaseModel):
    status: RoomStatus


class RoomResponseSchema(BaseModel):
    room_id: int
    ward_id: int
    room_number: str
    room_type: str
    status: str
    floor_number: Optional[int] = None
    created_at: datetime
