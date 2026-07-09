from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


class ChronicConditionCreateSchema(BaseModel):
    patient_id: int
    condition_name: str = Field(..., min_length=2, max_length=150)
    diagnosis_date: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=255)


class ChronicConditionUpdateSchema(BaseModel):
    condition_name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    diagnosis_date: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=255)


class ChronicConditionResponseSchema(BaseModel):
    condition_id: int
    patient_id: int
    condition_name: str
    diagnosis_date: Optional[date] = None
    notes: Optional[str] = None
