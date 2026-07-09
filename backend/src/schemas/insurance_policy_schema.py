from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class InsurancePolicyCreateSchema(BaseModel):
    patient_id: int
    provider_id: int
    policy_number: str = Field(..., min_length=3, max_length=100)
    coverage_percentage: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True


class InsurancePolicyUpdateSchema(BaseModel):
    provider_id: Optional[int] = None
    policy_number: Optional[str] = Field(default=None, min_length=3, max_length=100)
    coverage_percentage: Optional[Decimal] = Field(default=None, ge=0, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


class InsurancePolicyResponseSchema(BaseModel):
    policy_id: int
    patient_id: int
    provider_id: int
    policy_number: str
    coverage_percentage: Decimal
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool
