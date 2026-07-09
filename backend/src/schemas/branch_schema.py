from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class BranchCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    address: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    is_active: bool = True


class BranchUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    address: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class BranchResponseSchema(BaseModel):
    branch_id: int
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool
    created_at: datetime
