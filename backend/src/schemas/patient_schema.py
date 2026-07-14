from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class PatientCreateSchema(BaseModel):
    mrn: str = Field(..., min_length=2, max_length=50)  # Medical Record Number
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: date
    gender: str = Field(..., min_length=1, max_length=10)
    national_id: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    emergency_contact_name: Optional[str] = Field(default=None, max_length=150)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=20)


class PatientUpdateSchema(BaseModel):
    mrn: Optional[str] = Field(default=None, min_length=2, max_length=50)
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(default=None, min_length=1, max_length=10)
    national_id: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    emergency_contact_name: Optional[str] = Field(default=None, max_length=150)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=20)


class PatientResponseSchema(BaseModel):
    patient_id: int
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    national_id: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime
