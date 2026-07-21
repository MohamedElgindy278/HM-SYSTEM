from config.database import get_pyodbc_connection
from schemas.dashboard_schema import DashboardStatsResponseSchema
from src.core.decorators import handle_db_errors


class DashboardService:

    @staticmethod
    @handle_db_errors("Failed to retrieve dashboard statistics")
    def get_dashboard_stats() -> DashboardStatsResponseSchema:

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("EXEC sp_GetDashboardStatistics")

            row = cursor.fetchone()

            return DashboardStatsResponseSchema(
                total_patients=row.total_patients,
                total_patients_trend=row.total_patients_trend,
                total_doctors=row.total_doctors,
                total_doctors_trend=row.total_doctors_trend,
                appointments_today=row.appointments_today,
                available_beds=row.available_beds,
                today_revenue=row.today_revenue,
                today_revenue_trend=row.today_revenue_trend,
                emergency_cases=row.emergency_cases,
            )
