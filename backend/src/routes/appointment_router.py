from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.appointment_schema import (
    AppointmentCreateSchema,
    AppointmentUpdateSchema,
)
from src.services.appointment_service import AppointmentService

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

# ==========================
# Available Slots
# ==========================


@router.get(
    "/available-slots",
    dependencies=[Depends(require_permission("appointment:read"))],
)
def get_available_slots(doctor_id: int, appointment_date: date):

    return Responses.ok(
        data=AppointmentService.get_available_slots(doctor_id, appointment_date),
    )


# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("appointment:create"))],
)
def create_appointment(appointment_data: AppointmentCreateSchema):

    AppointmentService.create_appointment(appointment_data)

    return Responses.created(message="Appointment created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("appointment:read"))],
)
def get_all_appointments(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    doctor_id: Optional[int] = Query(default=None),
    patient_id: Optional[int] = Query(default=None),
    status: Optional[str] = Query(default=None),
    from_date: Optional[date] = Query(default=None),
    to_date: Optional[date] = Query(default=None),
):

    return Responses.ok(
        data=AppointmentService.get_all_appointments(
            start_num,
            page_size,
            doctor_id,
            patient_id,
            status,
            from_date,
            to_date,
        ),
    )


@router.get(
    "/{appointment_id}",
    dependencies=[Depends(require_permission("appointment:read"))],
)
def get_appointment_by_id(appointment_id: int):

    return Responses.ok(
        data=AppointmentService.get_appointment_by_id(appointment_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{appointment_id}",
    dependencies=[Depends(require_permission("appointment:update"))],
)
def update_appointment(appointment_id: int, appointment_data: AppointmentUpdateSchema):

    AppointmentService.update_appointment(appointment_id, appointment_data)

    return Responses.ok(message="Appointment updated successfully")


# ==========================
# Cancel
# ==========================


@router.put(
    "/{appointment_id}/cancel",
    dependencies=[Depends(require_permission("appointment:cancel"))],
)
def cancel_appointment(appointment_id: int):

    AppointmentService.cancel_appointment(appointment_id)

    return Responses.ok(message="Appointment cancelled successfully")


# ==========================
# Complete
# ==========================


@router.put(
    "/{appointment_id}/complete",
    dependencies=[Depends(require_permission("appointment:complete"))],
)
def complete_appointment(appointment_id: int):

    AppointmentService.complete_appointment(appointment_id)

    return Responses.ok(message="Appointment completed successfully")
