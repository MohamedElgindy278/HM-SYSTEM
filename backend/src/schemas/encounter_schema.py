from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class EncounterCreateSchema(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    branch_id: int
    encounter_type: str = Field(..., min_length=2, max_length=20)
    encounter_date: datetime
    chief_complaint: Optional[str] = Field(default=None, max_length=255)
    diagnosis: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = Field(default=None, max_length=500)


class EncounterUpdateSchema(BaseModel):
    doctor_id: Optional[int] = None
    appointment_id: Optional[int] = None
    branch_id: Optional[int] = None
    encounter_type: Optional[str] = Field(default=None, min_length=2, max_length=20)
    encounter_date: Optional[datetime] = None
    chief_complaint: Optional[str] = Field(default=None, max_length=255)
    diagnosis: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = Field(default=None, max_length=500)


class EncounterResponseSchema(BaseModel):
    encounter_id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    branch_id: int
    encounter_type: str
    encounter_date: datetime
    chief_complaint: Optional[str] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
