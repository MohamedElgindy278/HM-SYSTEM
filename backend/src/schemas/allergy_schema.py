from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


class AllergyCreateSchema(BaseModel):
    patient_id: int
    allergen_name: str = Field(..., min_length=2, max_length=150)
    reaction: Optional[str] = Field(default=None, max_length=255)
    severity: Optional[str] = Field(default=None, max_length=20)
    recorded_date: Optional[date] = None


class AllergyUpdateSchema(BaseModel):
    allergen_name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    reaction: Optional[str] = Field(default=None, max_length=255)
    severity: Optional[str] = Field(default=None, max_length=20)
    recorded_date: Optional[date] = None


class AllergyResponseSchema(BaseModel):
    allergy_id: int
    patient_id: int
    allergen_name: str
    reaction: Optional[str] = None
    severity: Optional[str] = None
    recorded_date: Optional[date] = None
