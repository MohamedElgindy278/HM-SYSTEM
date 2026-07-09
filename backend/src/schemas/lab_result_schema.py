from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LabResultCreateSchema(BaseModel):
    lab_test_id: int
    result_value: Optional[str] = Field(default=None, max_length=255)
    unit: Optional[str] = Field(default=None, max_length=50)
    reference_range: Optional[str] = Field(default=None, max_length=100)
    performed_by_user_id: Optional[int] = None
    result_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=255)


class LabResultUpdateSchema(BaseModel):
    result_value: Optional[str] = Field(default=None, max_length=255)
    unit: Optional[str] = Field(default=None, max_length=50)
    reference_range: Optional[str] = Field(default=None, max_length=100)
    performed_by_user_id: Optional[int] = None
    result_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=255)


class LabResultResponseSchema(BaseModel):
    lab_result_id: int
    lab_test_id: int
    result_value: Optional[str] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    performed_by_user_id: Optional[int] = None
    result_date: Optional[datetime] = None
    notes: Optional[str] = None
