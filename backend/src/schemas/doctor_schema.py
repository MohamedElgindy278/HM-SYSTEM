from typing import Optional

from pydantic import Field, BaseModel


class DoctorCreateSchema(BaseModel):
    user_id: int
    specialty_id: int
    license_number: str = Field(..., min_length=3, max_length=100)
    years_of_experience: int = Field(..., ge=0)


class DoctorUpdateSchema(BaseModel):
    user_id: Optional[int] = None
    specialty_id: Optional[int] = None
    license_number: Optional[str] = Field(default=None, min_length=3, max_length=100)
    years_of_experience: Optional[int] = Field(default=None, ge=0)


class DoctorResponseSchema(BaseModel):
    doctor_id: int
    user_id: int
    specialty_id: int
    license_number: str
    years_of_experience: Optional[int] = None
