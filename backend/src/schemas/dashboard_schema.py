from pydantic import BaseModel


class DashboardStatItemSchema(BaseModel):
    value: int | float
    trend: float


class DashboardStatsResponseSchema(BaseModel):
    total_patients: DashboardStatItemSchema
    total_doctors: DashboardStatItemSchema
    appointments_today: DashboardStatItemSchema
    available_beds: DashboardStatItemSchema
    today_revenue: DashboardStatItemSchema
    emergency_cases: DashboardStatItemSchema
