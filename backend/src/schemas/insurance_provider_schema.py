from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class InsuranceProviderCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None


class InsuranceProviderUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None


class InsuranceProviderResponseSchema(BaseModel):
    provider_id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
