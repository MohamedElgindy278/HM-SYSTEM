from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class InvoiceItemCreateSchema(BaseModel):
    invoice_id: int
    item_description: str = Field(..., min_length=2, max_length=255)
    item_type: Optional[str] = Field(default=None, max_length=50)
    quantity: int = Field(default=1, ge=1)
    unit_price: Decimal = Field(..., ge=0)
    insurance_coverage_percentage: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    line_total: Decimal = Field(..., ge=0)


class InvoiceItemUpdateSchema(BaseModel):
    item_description: Optional[str] = Field(default=None, min_length=2, max_length=255)
    item_type: Optional[str] = Field(default=None, max_length=50)
    quantity: Optional[int] = Field(default=None, ge=1)
    unit_price: Optional[Decimal] = Field(default=None, ge=0)
    insurance_coverage_percentage: Optional[Decimal] = Field(default=None, ge=0, le=100)
    line_total: Optional[Decimal] = Field(default=None, ge=0)


class InvoiceItemResponseSchema(BaseModel):
    invoice_item_id: int
    invoice_id: int
    item_description: str
    item_type: Optional[str] = None
    quantity: int
    unit_price: Decimal
    insurance_coverage_percentage: Decimal
    line_total: Decimal
