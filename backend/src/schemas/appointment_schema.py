from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AppointmentCreateSchema(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    appointment_date: datetime
    notes: Optional[str] = Field(default=None, max_length=255)
    # clinic_id removed — derived automatically from Doctor.clinic_id

    @field_validator("appointment_date")
    @classmethod
    def reject_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is not None:
            raise ValueError(
                "appointment_date must be a naive local datetime (no timezone offset)."
            )
        return value


class AppointmentUpdateSchema(BaseModel):
    doctor_id: Optional[int] = Field(default=None, gt=0)
    appointment_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=255)
    # clinic_id removed — re-derived automatically ONLY if doctor_id changes

    @field_validator("appointment_date")
    @classmethod
    def reject_timezone_aware(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is not None and value.tzinfo is not None:
            raise ValueError(
                "appointment_date must be a naive local datetime (no timezone offset)."
            )
        return value


class AppointmentResponseSchema(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    clinic_id: Optional[int] = None
    appointment_date: datetime
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
