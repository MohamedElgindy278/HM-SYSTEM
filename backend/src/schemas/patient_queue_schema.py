from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

QueueStatus = Literal["Waiting", "InProgress", "Completed", "NoShow"]


class PatientQueueCheckInSchema(BaseModel):
    appointment_id: int


class PatientQueueResponseSchema(BaseModel):
    queue_id: int
    patient_id: int
    clinic_id: int
    appointment_id: int
    check_in_time: datetime
    called_time: Optional[datetime] = None
    status: QueueStatus


class PatientQueueEmergencyCheckInSchema(BaseModel):
    patient_id: int
    clinic_id: int  
