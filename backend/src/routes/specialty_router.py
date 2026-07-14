from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.specialty_schema import (
    SpecialtyCreateSchema,
    SpecialtyUpdateSchema,
)
from src.services.specialty_service import SpecialtyService

router = APIRouter(
    prefix="/specialties",
    tags=["Specialties"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("specialty:create"))],
)
def create_specialty(specialty_data: SpecialtyCreateSchema):

    SpecialtyService.create_specialty(specialty_data)

    return Responses.created(message="Specialty created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("specialty:read"))],
)
def get_all_specialties(
    department_id: Optional[int] = Query(default=None),
):

    return Responses.ok(
        data=SpecialtyService.get_all_specialties(department_id),
    )


@router.get(
    "/{specialty_id}",
    dependencies=[Depends(require_permission("specialty:read"))],
)
def get_specialty_by_id(specialty_id: int):

    return Responses.ok(
        data=SpecialtyService.get_specialty_by_id(specialty_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{specialty_id}",
    dependencies=[Depends(require_permission("specialty:update"))],
)
def update_specialty(specialty_id: int, specialty_data: SpecialtyUpdateSchema):

    SpecialtyService.update_specialty(specialty_id, specialty_data)

    return Responses.ok(message="Specialty updated successfully")
