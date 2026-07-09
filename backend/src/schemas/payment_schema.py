from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PaymentCreateSchema(BaseModel):
    invoice_id: int
    amount: Decimal = Field(..., ge=0)
    payment_method: Optional[str] = Field(default=None, max_length=30)
    payer_type: Optional[str] = Field(default=None, max_length=20)
    payment_date: datetime
    reference_number: Optional[str] = Field(default=None, max_length=100)


class PaymentUpdateSchema(BaseModel):
    amount: Optional[Decimal] = Field(default=None, ge=0)
    payment_method: Optional[str] = Field(default=None, max_length=30)
    payer_type: Optional[str] = Field(default=None, max_length=20)
    payment_date: Optional[datetime] = None
    reference_number: Optional[str] = Field(default=None, max_length=100)


class PaymentResponseSchema(BaseModel):
    payment_id: int
    invoice_id: int
    amount: Decimal
    payment_method: Optional[str] = None
    payer_type: Optional[str] = None
    payment_date: datetime
    reference_number: Optional[str] = None
