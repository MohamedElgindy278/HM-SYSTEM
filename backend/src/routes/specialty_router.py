from fastapi import APIRouter

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


@router.post("/")
def create_specialty(specialty_data: SpecialtyCreateSchema):

    SpecialtyService.create_specialty(
        specialty_data,
    )

    return Responses.ok(
        message="Specialty created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("/")
def get_all_specialties():

    return Responses.ok(
        data=SpecialtyService.get_all_specialties(),
    )


@router.get("/{specialty_id}")
def get_specialty_by_id(specialty_id: int):

    return Responses.ok(
        data=SpecialtyService.get_specialty_by_id(specialty_id),
    )


# ==========================
# Update
# ==========================


@router.put("/{specialty_id}")
def update_specialty(
    specialty_id: int,
    specialty_data: SpecialtyUpdateSchema,
):

    SpecialtyService.update_specialty(
        specialty_id,
        specialty_data,
    )

    return Responses.ok(
        message="Specialty updated successfully",
    )
