from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AppointmentCreateSchema(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str = Field(default="Scheduled", max_length=20)
    notes: Optional[str] = Field(default=None, max_length=255)


class AppointmentUpdateSchema(BaseModel):
    doctor_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    status: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=255)


class AppointmentResponseSchema(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str
    notes: Optional[str] = None
    created_at: datetime
