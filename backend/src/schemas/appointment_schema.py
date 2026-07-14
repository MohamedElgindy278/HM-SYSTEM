from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AppointmentCreateSchema(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    notes: Optional[str] = Field(default=None, max_length=255)

    @field_validator("appointment_date")
    @classmethod
    def strip_timezone(cls, value: datetime) -> datetime:
        return value.replace(tzinfo=None)


class AppointmentUpdateSchema(BaseModel):
    doctor_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=255)

    @field_validator("appointment_date")
    @classmethod
    def strip_timezone(cls, value: Optional[datetime]) -> Optional[datetime]:
        return value.replace(tzinfo=None) if value is not None else value


class AppointmentResponseSchema(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
