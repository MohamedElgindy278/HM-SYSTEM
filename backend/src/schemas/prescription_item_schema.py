from typing import Optional
from pydantic import BaseModel, Field


class PrescriptionItemCreateSchema(BaseModel):
    prescription_id: int
    medication_id: int
    dosage: Optional[str] = Field(default=None, max_length=100)
    frequency: Optional[str] = Field(default=None, max_length=100)
    duration_days: Optional[int] = Field(default=None, ge=1)
    instructions: Optional[str] = Field(default=None, max_length=255)


class PrescriptionItemUpdateSchema(BaseModel):
    medication_id: Optional[int] = None
    dosage: Optional[str] = Field(default=None, max_length=100)
    frequency: Optional[str] = Field(default=None, max_length=100)
    duration_days: Optional[int] = Field(default=None, ge=1)
    instructions: Optional[str] = Field(default=None, max_length=255)


class PrescriptionItemResponseSchema(BaseModel):
    prescription_item_id: int
    prescription_id: int
    medication_id: int
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration_days: Optional[int] = None
    instructions: Optional[str] = None
