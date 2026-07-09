from fastapi import APIRouter

from src.core.responses import Responses
from src.schemas.doctor_schedule_schema import (
    DoctorScheduleCreateSchema,
    DoctorScheduleUpdateSchema,
)
from src.services.doctor_schedule_service import (
    DoctorScheduleService,
)

router = APIRouter(
    prefix="/doctor-schedules",
    tags=["Doctor Schedules"],
)

# ==========================
# Create
# ==========================


@router.post("")
def create_doctor_schedule(
    schedule_data: DoctorScheduleCreateSchema,
):

    DoctorScheduleService.create_doctor_schedule(
        schedule_data,
    )

    return Responses.ok(
        message="Doctor schedule created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("")
def get_all_doctor_schedules():

    return Responses.ok(
        data=DoctorScheduleService.get_all_doctor_schedules(),
    )


@router.get("/{schedule_id}")
def get_doctor_schedule_by_id(
    schedule_id: int,
):

    return Responses.ok(
        data=DoctorScheduleService.get_doctor_schedule_by_id(
            schedule_id,
        )
    )


# ==========================
# Update
# ==========================


@router.put("/{schedule_id}")
def update_doctor_schedule(
    schedule_id: int,
    schedule_data: DoctorScheduleUpdateSchema,
):

    DoctorScheduleService.update_doctor_schedule(
        schedule_id,
        schedule_data,
    )

    return Responses.ok(
        message="Doctor schedule updated successfully",
    )
