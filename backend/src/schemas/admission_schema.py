from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AdmissionCreateSchema(BaseModel):
    patient_id: int
    encounter_id: int
    bed_id: int
    attending_doctor_id: int
    admission_date: datetime
    expected_discharge_date: Optional[datetime] = None
    status: str = Field(default="Admitted", max_length=20)


class AdmissionUpdateSchema(BaseModel):
    bed_id: Optional[int] = None
    attending_doctor_id: Optional[int] = None
    expected_discharge_date: Optional[datetime] = None
    actual_discharge_date: Optional[datetime] = None
    status: Optional[str] = Field(default=None, max_length=20)


class AdmissionResponseSchema(BaseModel):
    admission_id: int
    patient_id: int
    encounter_id: int
    bed_id: int
    attending_doctor_id: int
    admission_date: datetime
    expected_discharge_date: Optional[datetime] = None
    actual_discharge_date: Optional[datetime] = None
    status: str
