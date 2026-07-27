from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.patient_queue_schema import (
    PatientQueueCheckInSchema,
    PatientQueueEmergencyCheckInSchema,
)
from src.services.patient_queue_service import PatientQueueService

router = APIRouter(
    prefix="/patient-queue",
    tags=["Patient Queue"],
)


@router.post(
    "/check-in",
    status_code=201,
    dependencies=[Depends(require_permission("patient_queue:checkin"))],
)
def check_in(check_in_data: PatientQueueCheckInSchema):

    PatientQueueService.check_in(check_in_data)

    return Responses.created(message="Patient checked in successfully")


@router.put(
    "/{queue_id}/call",
    dependencies=[Depends(require_permission("patient_queue:call"))],
)
def call_patient(queue_id: int):

    PatientQueueService.call_patient(queue_id)

    return Responses.ok(message="Patient called successfully")


@router.put(
    "/{queue_id}/no-show",
    dependencies=[Depends(require_permission("patient_queue:call"))],
)
def mark_no_show(queue_id: int):

    PatientQueueService.mark_no_show(queue_id)

    return Responses.ok(message="Patient marked as no-show")


@router.get(
    "",
    dependencies=[Depends(require_permission("patient_queue:read"))],
)
def get_clinic_queue(
    clinic_id: int,
    status: Optional[str] = Query(default=None),
):

    return Responses.ok(
        data=PatientQueueService.get_clinic_queue(clinic_id, status),
    )


@router.post(
    "/emergency-check-in",
    status_code=201,
    dependencies=[Depends(require_permission("patient_queue:checkin"))],
)
def emergency_check_in(data: PatientQueueEmergencyCheckInSchema):

    PatientQueueService.emergency_check_in(data)

    return Responses.created(message="Emergency patient checked in successfully")
