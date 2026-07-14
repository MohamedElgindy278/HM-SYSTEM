from fastapi import APIRouter, Query, Depends

from src.core.responses import Responses
from src.schemas.patient_schema import (
    PatientCreateSchema,
    PatientUpdateSchema,
)
from src.services.patient_service import PatientService
from src.core.deps import require_permission

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("patient:create"))],
)
def create_patient(patient_data: PatientCreateSchema):

    PatientService.create_patient(patient_data)

    return Responses.created(message="Patient created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("patient:read"))],
)
def get_all_patients(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return Responses.ok(data=PatientService.get_all_patients(start_num, page_size))


@router.get(
    "/{patient_id}",
    dependencies=[Depends(require_permission("patient:read"))],
)
def get_patient_by_id(patient_id: int):

    return Responses.ok(
        data=PatientService.get_patient_by_id(patient_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{patient_id}",
    dependencies=[Depends(require_permission("patient:update"))],
)
def update_patient(patient_id: int, patient_data: PatientUpdateSchema):

    PatientService.update_patient(patient_id, patient_data)

    return Responses.ok(message="Patient updated successfully")


# ==========================
# Delete
# ==========================


@router.delete(
    "/{patient_id}",
    dependencies=[Depends(require_permission("patient:delete"))],
)
def delete_patient(patient_id: int):

    PatientService.delete_patient(patient_id)

    return Responses.deleted(message="Patient deleted successfully")
