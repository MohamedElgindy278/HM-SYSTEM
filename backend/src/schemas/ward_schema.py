from typing import Optional
from pydantic import BaseModel, Field


class WardCreateSchema(BaseModel):
    department_id: int
    name: str = Field(..., min_length=2, max_length=100)
    floor_number: Optional[int] = Field(default=None, ge=0)
    ward_type: Optional[str] = Field(default=None, max_length=50)


class WardUpdateSchema(BaseModel):
    department_id: Optional[int] = None
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    floor_number: Optional[int] = Field(default=None, ge=0)
    ward_type: Optional[str] = Field(default=None, max_length=50)


class WardResponseSchema(BaseModel):
    ward_id: int
    department_id: int
    name: str
    floor_number: Optional[int] = None
    ward_type: Optional[str] = None
