from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PrescriptionCreateSchema(BaseModel):
    encounter_id: int
    doctor_id: int
    prescription_date: datetime
    notes: Optional[str] = Field(default=None, max_length=255)


class PrescriptionUpdateSchema(BaseModel):
    prescription_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=255)


class PrescriptionResponseSchema(BaseModel):
    prescription_id: int
    encounter_id: int
    doctor_id: int
    prescription_date: datetime
    notes: Optional[str] = None
