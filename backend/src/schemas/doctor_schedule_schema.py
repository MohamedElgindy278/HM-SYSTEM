from datetime import datetime, time
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

DayOfWeek = Literal[
    "Saturday",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
]


class DoctorScheduleCreateSchema(BaseModel):
    doctor_id: int
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    is_active: bool = True

    @model_validator(mode="after")
    def check_times(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        return self


class DoctorScheduleUpdateSchema(BaseModel):
    day_of_week: Optional[DayOfWeek] = None
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
    created_at: datetime
    updated_at: datetime
