from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ClinicCreateSchema(BaseModel):
    department_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=100)
    room_number: Optional[str] = Field(default=None, max_length=20)
    floor_number: Optional[int] = Field(default=None, ge=0)
    is_active: bool = True


class ClinicUpdateSchema(BaseModel):
    department_id: Optional[int] = Field(default=None, gt=0)
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    room_number: Optional[str] = Field(default=None, max_length=20)
    floor_number: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class ClinicResponseSchema(BaseModel):
    clinic_id: int
    department_id: int
    name: str
    room_number: Optional[str] = None
    floor_number: Optional[int] = None
    is_active: bool
    created_at: datetime
