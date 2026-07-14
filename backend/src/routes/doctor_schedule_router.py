from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import get_current_user, require_permission
from src.core.responses import Responses
from src.schemas.auth_schema import CurrentUserSchema
from src.schemas.doctor_schedule_schema import (
    DoctorScheduleCreateSchema,
    DoctorScheduleUpdateSchema,
)
from src.services.doctor_schedule_service import DoctorScheduleService

router = APIRouter(
    prefix="/doctor-schedules",
    tags=["Doctor Schedules"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("doctor_schedule:create"))],
)
def create_doctor_schedule(schedule_data: DoctorScheduleCreateSchema):

    DoctorScheduleService.create_doctor_schedule(schedule_data)

    return Responses.created(message="Doctor schedule created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("doctor_schedule:read"))],
)
def get_all_doctor_schedules(
    doctor_id: Optional[int] = Query(default=None),
):

    return Responses.ok(
        data=DoctorScheduleService.get_all_doctor_schedules(doctor_id),
    )


@router.get(
    "/{schedule_id}",
    dependencies=[Depends(require_permission("doctor_schedule:read"))],
)
def get_doctor_schedule_by_id(schedule_id: int):

    return Responses.ok(
        data=DoctorScheduleService.get_doctor_schedule_by_id(schedule_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{schedule_id}",
    dependencies=[Depends(require_permission("doctor_schedule:update"))],
)
def update_doctor_schedule(
    schedule_id: int,
    schedule_data: DoctorScheduleUpdateSchema,
    current_user: CurrentUserSchema = Depends(get_current_user),
):

    DoctorScheduleService.update_doctor_schedule(
        schedule_id, schedule_data, current_user
    )

    return Responses.ok(message="Doctor schedule updated successfully")
