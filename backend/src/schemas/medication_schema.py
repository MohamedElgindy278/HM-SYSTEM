from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class MedicationCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    form: Optional[str] = Field(default=None, max_length=50)
    strength: Optional[str] = Field(default=None, max_length=50)
    manufacturer: Optional[str] = Field(default=None, max_length=150)
    unit_price: Decimal = Field(default=Decimal("0"), ge=0)


class MedicationUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    form: Optional[str] = Field(default=None, max_length=50)
    strength: Optional[str] = Field(default=None, max_length=50)
    manufacturer: Optional[str] = Field(default=None, max_length=150)
    unit_price: Optional[Decimal] = Field(default=None, ge=0)


class MedicationResponseSchema(BaseModel):
    medication_id: int
    name: str
    form: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None
    unit_price: Decimal
