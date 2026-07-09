from datetime import time
from typing import Optional

from pydantic import BaseModel, Field


class DoctorScheduleCreateSchema(BaseModel):
    doctor_id: int
    day_of_week: str = Field(..., max_length=20)
    start_time: time
    end_time: time
    is_active: bool = True


class DoctorScheduleUpdateSchema(BaseModel):
    day_of_week: Optional[str] = Field(default=None, max_length=20)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None


class DoctorScheduleResponseSchema(BaseModel):
    schedule_id: int
    doctor_id: int
    day_of_week: str
    start_time: time
    end_time: time
    is_active: bool
