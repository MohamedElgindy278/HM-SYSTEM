from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

Gender = Literal["Male", "Female", "Other"]


class PatientCreateSchema(BaseModel):
    # mrn is NOT accepted here — system-generated (format: MRN-00001)
    # by the TR_CreateMRN trigger right after insertion.
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: date
    gender: Gender
    national_id: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    emergency_contact_name: Optional[str] = Field(default=None, max_length=150)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=20)

    @field_validator("date_of_birth")
    @classmethod
    def reject_future_dob(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("date_of_birth cannot be in the future.")
        return value


class PatientUpdateSchema(BaseModel):
    # mrn intentionally excluded — system-generated identifier,
    # immutable after creation.
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    national_id: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    emergency_contact_name: Optional[str] = Field(default=None, max_length=150)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=20)

    @field_validator("date_of_birth")
    @classmethod
    def reject_future_dob(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value > date.today():
            raise ValueError("date_of_birth cannot be in the future.")
        return value


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
