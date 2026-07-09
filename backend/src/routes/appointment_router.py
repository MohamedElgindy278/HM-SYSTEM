from datetime import date

from fastapi import APIRouter

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


@router.get("/available-slots")
def get_available_slots(
    doctor_id: int,
    appointment_date: date,
):

    return Responses.ok(
        data=AppointmentService.get_available_slots(
            doctor_id,
            appointment_date,
        ),
    )


# ==========================
# Create
# ==========================


@router.post("")
def create_appointment(
    appointment_data: AppointmentCreateSchema,
):

    AppointmentService.create_appointment(
        appointment_data,
    )

    return Responses.ok(
        message="Appointment created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("")
def get_all_appointments():

    return Responses.ok(
        data=AppointmentService.get_all_appointments(),
    )


@router.get("/{appointment_id}")
def get_appointment_by_id(
    appointment_id: int,
):

    return Responses.ok(
        data=AppointmentService.get_appointment_by_id(
            appointment_id,
        ),
    )


# ==========================
# Update
# ==========================


@router.put("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdateSchema,
):

    AppointmentService.update_appointment(
        appointment_id,
        appointment_data,
    )

    return Responses.ok(
        message="Appointment updated successfully",
    )


# ==========================
# Cancel
# ==========================


@router.put("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
):

    AppointmentService.cancel_appointment(
        appointment_id,
    )

    return Responses.ok(
        message="Appointment cancelled successfully",
    )


# ==========================
# Complete
# ==========================


@router.put("/{appointment_id}/complete")
def complete_appointment(
    appointment_id: int,
):

    AppointmentService.complete_appointment(
        appointment_id,
    )

    return Responses.ok(
        message="Appointment completed successfully",
    )
