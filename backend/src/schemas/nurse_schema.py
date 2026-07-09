from typing import Optional

from pydantic import BaseModel, Field


class NurseCreateSchema(BaseModel):
    user_id: int
    department_id: int
    license_number: str = Field(..., min_length=3, max_length=100)


class NurseUpdateSchema(BaseModel):
    user_id: Optional[int] = None
    department_id: Optional[int] = None
    license_number: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
    )


class NurseResponseSchema(BaseModel):
    nurse_id: int
    user_id: int
    department_id: int
    license_number: Optional[str] = None
