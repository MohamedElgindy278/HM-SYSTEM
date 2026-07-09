from typing import Optional
from pydantic import BaseModel, Field


class BedCreateSchema(BaseModel):
    ward_id: int
    bed_number: str = Field(..., min_length=1, max_length=20)
    status: str = Field(default="Available", max_length=20)


class BedUpdateSchema(BaseModel):
    ward_id: Optional[int] = None
    bed_number: Optional[str] = Field(default=None, min_length=1, max_length=20)
    status: Optional[str] = Field(default=None, max_length=20)


class BedResponseSchema(BaseModel):
    bed_id: int
    ward_id: int
    bed_number: str
    status: str
