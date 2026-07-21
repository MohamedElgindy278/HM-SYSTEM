from fastapi import APIRouter

from services.dashboard_service import DashboardService
from schemas.dashboard_schema import DashboardStatsResponseSchema

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/stats",
    response_model=DashboardStatsResponseSchema,
    summary="Get dashboard statistics",
)
def get_dashboard_statistics():
    return DashboardService.get_dashboard_stats()
