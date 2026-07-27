from typing import Literal

from fastapi import APIRouter, Query

from src.core.responses import Responses
from src.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

PeriodParam = Literal["week", "month", "year"]


# ==========================
# Overview
# ==========================


@router.get("/stats", summary="Get dashboard statistics")
def get_dashboard_statistics():

    return Responses.ok(
        data=DashboardService.get_dashboard_stats(),
    )


@router.get("/hospital-status", summary="Get current hospital status")
def get_hospital_status():

    return Responses.ok(
        data=DashboardService.get_hospital_status(),
    )


@router.get("/today-appointments", summary="Get today's appointments (paginated)")
def get_today_appointments(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):

    return Responses.ok(
        data=DashboardService.get_today_appointments(start_num, page_size),
    )


@router.get("/recent-activity", summary="Get recent system activity feed")
def get_recent_activity(
    limit: int = Query(default=20, ge=1, le=100),
):

    return Responses.ok(
        data=DashboardService.get_recent_activity(limit),
    )


# ==========================
# Analytics / Charts
# ==========================


@router.get("/patient-growth", summary="Get patient growth trend")
def get_patient_growth(
    period: PeriodParam = Query(default="month"),
):

    return Responses.ok(
        data=DashboardService.get_patient_growth(period),
    )


@router.get("/revenue-analytics", summary="Get revenue trend")
def get_revenue_analytics(
    period: PeriodParam = Query(default="month"),
):

    return Responses.ok(
        data=DashboardService.get_revenue_analytics(period),
    )


@router.get("/appointments-analytics", summary="Get appointments breakdown by status")
def get_appointments_analytics(
    period: PeriodParam = Query(default="month"),
):

    return Responses.ok(
        data=DashboardService.get_appointments_analytics(period),
    )


@router.get(
    "/department-distribution", summary="Get patient distribution across departments"
)
def get_department_distribution():

    return Responses.ok(
        data=DashboardService.get_department_distribution(),
    )


@router.get("/bed-occupancy", summary="Get bed occupancy rate trend")
def get_bed_occupancy_analytics(
    period: PeriodParam = Query(default="month"),
):

    return Responses.ok(
        data=DashboardService.get_bed_occupancy_analytics(period),
    )


@router.get("/admissions-analytics", summary="Get admissions vs discharges trend")
def get_admissions_analytics(
    period: PeriodParam = Query(default="month"),
):

    return Responses.ok(
        data=DashboardService.get_admissions_analytics(period),
    )
