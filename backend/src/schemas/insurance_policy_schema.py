from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class InsurancePolicyCreateSchema(BaseModel):
    patient_id: int
    provider_id: int
    policy_number: str = Field(..., min_length=3, max_length=100)
    coverage_percentage: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


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
    created_at: datetime
    updated_at: datetime
