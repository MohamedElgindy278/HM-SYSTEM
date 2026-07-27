from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.clinic_schema import ClinicCreateSchema, ClinicUpdateSchema
from src.services.clinic_service import ClinicService

router = APIRouter(
    prefix="/clinics",
    tags=["Clinics"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("clinic:create"))],
)
def create_clinic(clinic_data: ClinicCreateSchema):

    ClinicService.create_clinic(clinic_data)

    return Responses.created(message="Clinic created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("clinic:read"))],
)
def get_all_clinics(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    department_id: Optional[int] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
):

    return Responses.ok(
        data=ClinicService.get_all_clinics(
            start_num,
            page_size,
            department_id,
            is_active,
        ),
    )


@router.get(
    "/{clinic_id}",
    dependencies=[Depends(require_permission("clinic:read"))],
)
def get_clinic_by_id(clinic_id: int):

    return Responses.ok(
        data=ClinicService.get_clinic_by_id(clinic_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{clinic_id}",
    dependencies=[Depends(require_permission("clinic:update"))],
)
def update_clinic(clinic_id: int, clinic_data: ClinicUpdateSchema):

    ClinicService.update_clinic(clinic_id, clinic_data)

    return Responses.ok(message="Clinic updated successfully")
