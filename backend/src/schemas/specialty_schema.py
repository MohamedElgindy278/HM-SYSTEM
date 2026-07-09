from typing import Optional
from pydantic import BaseModel, Field


class SpecialtyCreateSchema(BaseModel):
    department_id: int
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    appointment_duration: int = Field(..., ge=5, le=180)


class SpecialtyUpdateSchema(BaseModel):
    department_id: Optional[int] = None
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    appointment_duration: Optional[int] = Field(default=None, ge=5, le=180)


class SpecialtyResponseSchema(BaseModel):
    specialty_id: int
    department_id: int
    name: str
    description: Optional[str] = None
    appointment_duration: int
