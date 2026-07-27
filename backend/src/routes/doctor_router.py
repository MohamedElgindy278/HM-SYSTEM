from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
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


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("doctor:create"))],
)
def create_doctor(doctor_data: DoctorCreateSchema):

    DoctorService.create_doctor(doctor_data)

    return Responses.created(message="Doctor created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("doctor:read"))],
)
def get_all_doctors(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    specialty_id: Optional[int] = Query(default=None),
    branch_id: Optional[int] = Query(default=None),
    clinic_id: Optional[int] = Query(default=None),
):

    return Responses.ok(
        data=DoctorService.get_all_doctors(
            start_num, page_size, specialty_id, branch_id, clinic_id
        ),
    )


@router.get(
    "/{doctor_id}",
    dependencies=[Depends(require_permission("doctor:read"))],
)
def get_doctor_by_id(doctor_id: int):

    return Responses.ok(
        data=DoctorService.get_doctor_by_id(doctor_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{doctor_id}",
    dependencies=[Depends(require_permission("doctor:update"))],
)
def update_doctor(doctor_id: int, doctor_data: DoctorUpdateSchema):

    DoctorService.update_doctor(doctor_id, doctor_data)

    return Responses.ok(message="Doctor updated successfully")
