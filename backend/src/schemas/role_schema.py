from typing import Optional

from pydantic import BaseModel, Field


class RoleCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)


class RoleUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)


class RoleResponseSchema(BaseModel):
    role_id: int
    name: str
    description: Optional[str] = None
