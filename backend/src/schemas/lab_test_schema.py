from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LabTestCreateSchema(BaseModel):
    encounter_id: int
    test_name: str = Field(..., min_length=2, max_length=150)
    ordered_by_doctor_id: int
    ordered_date: datetime
    status: str = Field(default="Ordered", max_length=20)


class LabTestUpdateSchema(BaseModel):
    test_name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    ordered_by_doctor_id: Optional[int] = None
    ordered_date: Optional[datetime] = None
    status: Optional[str] = Field(default=None, max_length=20)


class LabTestResponseSchema(BaseModel):
    lab_test_id: int
    encounter_id: int
    test_name: str
    ordered_by_doctor_id: int
    ordered_date: datetime
    status: str
