from fastapi import APIRouter

from src.core.responses import Responses
from src.schemas.doctor_schema import (
    DoctorCreateSchema,
    DoctorUpdateSchema,
)
from src.services.doctor_service import DoctorService

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)

# ==========================
# Create
# ==========================


@router.post("")
def create_doctor(doctor_data: DoctorCreateSchema):

    DoctorService.create_doctor(
        doctor_data,
    )

    return Responses.ok(
        message="Doctor created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("")
def get_all_doctors():

    return Responses.ok(
        data=DoctorService.get_all_doctors(),
    )


@router.get("/{doctor_id}")
def get_doctor_by_id(doctor_id: int):

    return Responses.ok(
        data=DoctorService.get_doctor_by_id(
            doctor_id,
        )
    )


# ==========================
# Update
# ==========================


@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorUpdateSchema,
):

    DoctorService.update_doctor(
        doctor_id,
        doctor_data,
    )

    return Responses.ok(
        message="Doctor updated successfully",
    )
