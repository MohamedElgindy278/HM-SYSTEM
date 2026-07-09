from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class RadiologyResultCreateSchema(BaseModel):
    radiology_test_id: int
    findings: Optional[str] = Field(default=None, max_length=500)
    image_path: Optional[str] = Field(default=None, max_length=255)
    performed_by_user_id: Optional[int] = None
    result_date: Optional[datetime] = None


class RadiologyResultUpdateSchema(BaseModel):
    findings: Optional[str] = Field(default=None, max_length=500)
    image_path: Optional[str] = Field(default=None, max_length=255)
    performed_by_user_id: Optional[int] = None
    result_date: Optional[datetime] = None


class RadiologyResultResponseSchema(BaseModel):
    radiology_result_id: int
    radiology_test_id: int
    findings: Optional[str] = None
    image_path: Optional[str] = None
    performed_by_user_id: Optional[int] = None
    result_date: Optional[datetime] = None
