from datetime import datetime
from decimal import Decimal
from typing import List, Literal, Optional, Union

from pydantic import BaseModel

# ==========================================================
# Dashboard Statistics (sp_GetDashboardStatistics)
# ==========================================================


class DashboardStatItemSchema(BaseModel):
    value: Union[int, float]
    trend: Optional[float] = None


class DashboardStatsResponseSchema(BaseModel):
    total_patients: DashboardStatItemSchema
    total_doctors: DashboardStatItemSchema
    appointments_today: DashboardStatItemSchema
    available_beds: DashboardStatItemSchema
    today_revenue: DashboardStatItemSchema
    emergency_cases: DashboardStatItemSchema


# ==========================================================
# Hospital Status
# ==========================================================


class BedOccupancyCardSchema(BaseModel):
    occupancy_rate: float  # percentage (0-100)


class RoomOccupancyCardSchema(BaseModel):
    occupied: int
    total: int


class WardStatusCardSchema(BaseModel):
    total_wards: int


class ClinicStatusCardSchema(BaseModel):
    open_clinics: int


class EmergencyQueueCardSchema(BaseModel):
    waiting_patients: int


class HospitalAvailabilitySchema(BaseModel):
    status: Literal["Normal", "Busy", "Critical"]
    occupancy_rate: float


class HospitalStatusSchema(BaseModel):
    bed_occupancy: BedOccupancyCardSchema
    room_occupancy: RoomOccupancyCardSchema
    ward_status: WardStatusCardSchema
    clinic_status: ClinicStatusCardSchema
    emergency_queue: EmergencyQueueCardSchema
    hospital_availability: HospitalAvailabilitySchema


# ==========================================================
# Today's Appointments
# ==========================================================


class TodayAppointmentItemSchema(BaseModel):
    appointment_id: int
    appointment_date: datetime
    status: str
    notes: Optional[str] = None
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str


# ==========================================================
# Generic period data point (patient growth / revenue trends)
# ==========================================================


class PeriodDataPointSchema(BaseModel):
    label: str
    value: Union[int, float, Decimal]


# ==========================================================
# Bed Occupancy Analytics (sp_GetBedOccupancyAnalytics)
# ==========================================================


class BedOccupancyPointSchema(BaseModel):
    label: str
    occupied_beds: int
    total_beds: int
    occupancy_rate: float


# ==========================================================
# Appointments Analytics
# ==========================================================


class AppointmentsAnalyticsSchema(BaseModel):
    scheduled: int = 0
    completed: int = 0
    cancelled: int = 0


# ==========================================================
# Department Distribution
# ==========================================================


class DepartmentDistributionItemSchema(BaseModel):
    department_id: int
    department_name: str
    patient_count: int


# ==========================================================
# Admissions Analytics (Admissions vs Discharges)
# ==========================================================


class AdmissionsAnalyticsItemSchema(BaseModel):
    label: str
    admissions: int = 0
    discharges: int = 0


# ==========================================================
# Recent Activity Feed (AuditLog)
# ==========================================================


class RecentActivityItemSchema(BaseModel):
    audit_id: int
    table_name: str
    record_id: int
    action: str
    changed_by: Optional[int] = None
    changed_by_name: Optional[str] = None
    changed_at: datetime
