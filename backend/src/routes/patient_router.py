from fastapi import APIRouter

from src.core.responses import Responses
from src.schemas.patient_schema import (
    PatientCreateSchema,
    PatientUpdateSchema,
)
from src.services.patient_service import PatientService

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)

# ==========================
# Create
# ==========================


@router.post("/")
def create_patient(
    patient_data: PatientCreateSchema,
):

    PatientService.create_patient(
        patient_data,
    )

    return Responses.ok(
        message="Patient created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("/")
def get_all_patients():

    return Responses.ok(
        data=PatientService.get_all_patients(),
    )


@router.get("/{patient_id}")
def get_patient_by_id(
    patient_id: int,
):

    return Responses.ok(
        data=PatientService.get_patient_by_id(
            patient_id,
        ),
    )


# ==========================
# Update
# ==========================


@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    patient_data: PatientUpdateSchema,
):

    PatientService.update_patient(
        patient_id,
        patient_data,
    )

    return Responses.ok(
        message="Patient updated successfully",
    )
