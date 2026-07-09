from typing import Optional
from pydantic import BaseModel, Field


class DepartmentCreateSchema(BaseModel):
    branch_id: int
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=255)


class DepartmentUpdateSchema(BaseModel):
    branch_id: Optional[int] = None
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=255)


class DepartmentResponseSchema(BaseModel):
    department_id: int
    branch_id: int
    name: str
    description: Optional[str] = None
