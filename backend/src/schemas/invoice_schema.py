from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class InvoiceCreateSchema(BaseModel):
    patient_id: int
    encounter_id: Optional[int] = None
    admission_id: Optional[int] = None
    invoice_date: datetime
    total_amount: Decimal = Field(default=Decimal("0"), ge=0)
    insurance_covered_amount: Decimal = Field(default=Decimal("0"), ge=0)
    patient_due_amount: Decimal = Field(default=Decimal("0"), ge=0)
    status: str = Field(default="Open", max_length=20)


class InvoiceUpdateSchema(BaseModel):
    encounter_id: Optional[int] = None
    admission_id: Optional[int] = None
    invoice_date: Optional[datetime] = None
    total_amount: Optional[Decimal] = Field(default=None, ge=0)
    insurance_covered_amount: Optional[Decimal] = Field(default=None, ge=0)
    patient_due_amount: Optional[Decimal] = Field(default=None, ge=0)
    status: Optional[str] = Field(default=None, max_length=20)


class InvoiceResponseSchema(BaseModel):
    invoice_id: int
    patient_id: int
    encounter_id: Optional[int] = None
    admission_id: Optional[int] = None
    invoice_date: datetime
    total_amount: Decimal
    insurance_covered_amount: Decimal
    patient_due_amount: Decimal
    status: str
