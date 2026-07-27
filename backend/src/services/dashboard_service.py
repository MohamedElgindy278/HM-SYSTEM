from datetime import date, timedelta
from typing import List

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors, ExceptionFactory
from src.schemas.dashboard_schema import (
    AdmissionsAnalyticsItemSchema,
    AppointmentsAnalyticsSchema,
    BedOccupancyCardSchema,
    BedOccupancyPointSchema,
    ClinicStatusCardSchema,
    DashboardStatItemSchema,
    DashboardStatsResponseSchema,
    DepartmentDistributionItemSchema,
    EmergencyQueueCardSchema,
    HospitalAvailabilitySchema,
    HospitalStatusSchema,
    PeriodDataPointSchema,
    RecentActivityItemSchema,
    RoomOccupancyCardSchema,
    TodayAppointmentItemSchema,
    WardStatusCardSchema,
)
from src.schemas.common_schema import PaginatedResponse
from src.core.query_utils import paginate

VALID_PERIODS = {"week", "month", "year"}


BUSY_THRESHOLD = 50
CRITICAL_THRESHOLD = 85


class DashboardService:

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def _resolve_period(period: str):
        """
        Normalizes the `period` query param into a (start_date, end_date, group_by)
        tuple used across the analytics endpoints.

        - week  -> last 7 days,   grouped by day
        - month -> last 30 days,  grouped by day
        - year  -> last 12 months, grouped by month
        """

        period = (period or "month").lower()

        if period not in VALID_PERIODS:
            raise Errors.validation_error(
                "Invalid period. Must be one of: week, month, year",
            )

        today = date.today()

        if period == "week":
            start_date = today - timedelta(days=6)
            group_by = "day"
        elif period == "year":
            start_date = today.replace(day=1) - timedelta(days=365)
            group_by = "month"
        else:
            start_date = today - timedelta(days=29)
            group_by = "day"

        return start_date, today, group_by

    @staticmethod
    def _classify_availability(occupancy_rate: float) -> str:
        if occupancy_rate > CRITICAL_THRESHOLD:
            return "Critical"
        if occupancy_rate >= BUSY_THRESHOLD:
            return "Busy"
        return "Normal"

    # ======================================================
    # Dashboard Statistics (Stored Procedure)
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve dashboard statistics")
    def get_dashboard_stats() -> DashboardStatsResponseSchema:

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("EXEC sp_GetDashboardStatistics")

            row = cursor.fetchone()

            if not row:
                raise ExceptionFactory.server_error(
                    "Failed to retrieve dashboard statistics",
                )

            return DashboardStatsResponseSchema(
                total_patients=DashboardStatItemSchema(
                    value=row.total_patients,
                    trend=row.total_patients_trend,
                ),
                total_doctors=DashboardStatItemSchema(
                    value=row.total_doctors,
                    trend=row.total_doctors_trend,
                ),
                appointments_today=DashboardStatItemSchema(
                    value=row.appointments_today,
                    trend=None,
                ),
                available_beds=DashboardStatItemSchema(
                    value=row.available_beds,
                    trend=None,
                ),
                today_revenue=DashboardStatItemSchema(
                    value=row.today_revenue,
                    trend=row.today_revenue_trend,
                ),
                emergency_cases=DashboardStatItemSchema(
                    value=row.emergency_cases,
                    trend=None,
                ),
            )

    # ======================================================
    # Hospital Status — 6 cards
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve hospital status")
    def get_hospital_status() -> HospitalStatusSchema:

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            # ---- 1) Bed occupancy (all beds, regardless of room/ward) ----
            cursor.execute(
                "SELECT status, COUNT(*) AS total FROM [Bed] GROUP BY status"
            )
            bed_counts = {row.status: row.total for row in cursor.fetchall()}
            bed_total = sum(bed_counts.values())
            bed_occupied = bed_counts.get("Occupied", 0)
            bed_occupancy_rate = (
                round((bed_occupied / bed_total) * 100, 2) if bed_total else 0.0
            )

            # ---- 2) Room occupancy (all rooms, all types) ----
            cursor.execute(
                "SELECT status, COUNT(*) AS total FROM [Room] GROUP BY status"
            )
            room_counts = {row.status: row.total for row in cursor.fetchall()}
            room_total = sum(room_counts.values())
            room_occupied = room_counts.get("Occupied", 0)

            # ---- 3) Ward status (total configured wards - no is_active column yet) ----
            cursor.execute("SELECT COUNT(*) AS total FROM [Ward]")
            ward_total = cursor.fetchone().total

            # ---- 4) Clinic status (static is_active flag) ----
            cursor.execute("SELECT COUNT(*) AS total FROM [Clinic] WHERE is_active = 1")
            open_clinics = cursor.fetchone().total

            # ---- 5) Emergency queue ----
            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM [PatientQueue] pq
                INNER JOIN [Clinic] c ON pq.clinic_id = c.clinic_id
                INNER JOIN [Department] d ON c.department_id = d.department_id
                WHERE pq.status = 'Waiting'
                AND d.is_emergency = 1
                AND CAST(pq.check_in_time AS DATE) = CAST(GETDATE() AS DATE)
                """)
            emergency_waiting = cursor.fetchone().total

        availability_status = DashboardService._classify_availability(
            bed_occupancy_rate
        )

        return HospitalStatusSchema(
            bed_occupancy=BedOccupancyCardSchema(occupancy_rate=bed_occupancy_rate),
            room_occupancy=RoomOccupancyCardSchema(
                occupied=room_occupied, total=room_total
            ),
            ward_status=WardStatusCardSchema(total_wards=ward_total),
            clinic_status=ClinicStatusCardSchema(open_clinics=open_clinics),
            emergency_queue=EmergencyQueueCardSchema(
                waiting_patients=emergency_waiting
            ),
            hospital_availability=HospitalAvailabilitySchema(
                status=availability_status,
                occupancy_rate=bed_occupancy_rate,
            ),
        )

    # ======================================================
    # Today's Appointments
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve today's appointments")
    def get_today_appointments(
        start_num: int = 1,
        page_size: int = 10,
    ) -> PaginatedResponse[TodayAppointmentItemSchema]:

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM [Appointment]
                WHERE CAST(appointment_date AS DATE) = CAST(GETDATE() AS DATE)
                """)
            total = cursor.fetchone().total

            cursor.execute(
                """
                SELECT
                    a.appointment_id,
                    a.appointment_date,
                    a.status,
                    a.notes,
                    p.patient_id,
                    p.first_name AS patient_first_name,
                    p.last_name AS patient_last_name,
                    doc.doctor_id,
                    u.first_name AS doctor_first_name,
                    u.last_name AS doctor_last_name
                FROM [Appointment] a
                INNER JOIN [Patient] p ON a.patient_id = p.patient_id
                INNER JOIN [Doctor] doc ON a.doctor_id = doc.doctor_id
                INNER JOIN [User] u ON doc.user_id = u.user_id
                WHERE CAST(a.appointment_date AS DATE) = CAST(GETDATE() AS DATE)
                ORDER BY a.appointment_date
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                (offset, limit),
            )

            rows = cursor.fetchall()

        items = [
            TodayAppointmentItemSchema(
                appointment_id=row.appointment_id,
                appointment_date=row.appointment_date,
                status=row.status,
                notes=row.notes,
                patient_id=row.patient_id,
                patient_name=f"{row.patient_first_name} {row.patient_last_name}",
                doctor_id=row.doctor_id,
                doctor_name=f"{row.doctor_first_name} {row.doctor_last_name}",
            )
            for row in rows
        ]

        return PaginatedResponse(items=items, total=total)

    # ======================================================
    # Patient Growth (Line Chart)
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve patient growth data")
    def get_patient_growth(period: str = "month") -> List[PeriodDataPointSchema]:

        start_date, _, group_by = DashboardService._resolve_period(period)

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            if group_by == "month":
                cursor.execute(
                    """
                    SELECT
                        FORMAT(created_at, 'yyyy-MM') AS period_label,
                        COUNT(*) AS total
                    FROM [Patient]
                    WHERE created_at >= ?
                    GROUP BY FORMAT(created_at, 'yyyy-MM')
                    ORDER BY period_label
                    """,
                    (start_date,),
                )
            else:
                cursor.execute(
                    """
                    SELECT
                        CAST(created_at AS DATE) AS period_label,
                        COUNT(*) AS total
                    FROM [Patient]
                    WHERE created_at >= ?
                    GROUP BY CAST(created_at AS DATE)
                    ORDER BY period_label
                    """,
                    (start_date,),
                )

            rows = cursor.fetchall()

        return [
            PeriodDataPointSchema(label=str(row.period_label), value=row.total)
            for row in rows
        ]

    # ======================================================
    # Revenue Analytics (Line Chart)
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve revenue analytics")
    def get_revenue_analytics(period: str = "month") -> List[PeriodDataPointSchema]:

        start_date, _, group_by = DashboardService._resolve_period(period)

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            if group_by == "month":
                cursor.execute(
                    """
                    SELECT
                        FORMAT(payment_date, 'yyyy-MM') AS period_label,
                        SUM(amount) AS total
                    FROM [Payment]
                    WHERE payment_date >= ?
                    GROUP BY FORMAT(payment_date, 'yyyy-MM')
                    ORDER BY period_label
                    """,
                    (start_date,),
                )
            else:
                cursor.execute(
                    """
                    SELECT
                        CAST(payment_date AS DATE) AS period_label,
                        SUM(amount) AS total
                    FROM [Payment]
                    WHERE payment_date >= ?
                    GROUP BY CAST(payment_date AS DATE)
                    ORDER BY period_label
                    """,
                    (start_date,),
                )

            rows = cursor.fetchall()

        return [
            PeriodDataPointSchema(label=str(row.period_label), value=row.total or 0)
            for row in rows
        ]

    # ======================================================
    # Appointments Analytics
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve appointments analytics")
    def get_appointments_analytics(
        period: str = "month",
    ) -> AppointmentsAnalyticsSchema:

        start_date, _, _ = DashboardService._resolve_period(period)

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT status, COUNT(*) AS total
                FROM [Appointment]
                WHERE appointment_date >= ?
                GROUP BY status
                """,
                (start_date,),
            )

            rows = cursor.fetchall()

        counts = {row.status: row.total for row in rows}

        return AppointmentsAnalyticsSchema(
            scheduled=counts.get("Scheduled", 0),
            completed=counts.get("Completed", 0),
            cancelled=counts.get("Cancelled", 0),
        )

    # ======================================================
    # Department Distribution (Pie Chart - patients per department)
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve department distribution")
    def get_department_distribution() -> List[DepartmentDistributionItemSchema]:

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    dept.department_id,
                    dept.name AS department_name,
                    COUNT(DISTINCT e.patient_id) AS patient_count
                FROM [Department] dept
                LEFT JOIN [Specialty] s ON s.department_id = dept.department_id
                LEFT JOIN [Doctor] doc ON doc.specialty_id = s.specialty_id
                LEFT JOIN [Encounter] e ON e.doctor_id = doc.doctor_id
                GROUP BY dept.department_id, dept.name
                ORDER BY patient_count DESC
                """)

            rows = cursor.fetchall()

        return [
            DepartmentDistributionItemSchema(
                department_id=row.department_id,
                department_name=row.department_name,
                patient_count=row.patient_count,
            )
            for row in rows
        ]

    # ======================================================
    # Bed Occupancy Analytics (trend over time - Stored Procedure)
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve bed occupancy analytics")
    def get_bed_occupancy_analytics(
        period: str = "month",
    ) -> List[BedOccupancyPointSchema]:

        period = (period or "month").lower()

        if period not in VALID_PERIODS:
            raise Errors.validation_error(
                "Invalid period. Must be one of: week, month, year",
            )

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                "EXEC sp_GetBedOccupancyAnalytics @Period = ?",
                (period,),
            )

            rows = cursor.fetchall()

        return [
            BedOccupancyPointSchema(
                label=row.label,
                occupied_beds=row.occupied_beds,
                total_beds=row.total_beds,
                occupancy_rate=float(row.occupancy_rate),
            )
            for row in rows
        ]

    # ======================================================
    # Admissions Analytics (Admissions vs Discharges)
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve admissions analytics")
    def get_admissions_analytics(
        period: str = "month",
    ) -> List[AdmissionsAnalyticsItemSchema]:

        start_date, _, group_by = DashboardService._resolve_period(period)

        if group_by == "month":
            admission_expr = "FORMAT(admission_date, 'yyyy-MM')"
            discharge_expr = "FORMAT(actual_discharge_date, 'yyyy-MM')"
        else:
            admission_expr = "CAST(admission_date AS DATE)"
            discharge_expr = "CAST(actual_discharge_date AS DATE)"

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                f"""
                SELECT {admission_expr} AS period_label, COUNT(*) AS total
                FROM [Admission]
                WHERE admission_date >= ?
                GROUP BY {admission_expr}
                """,
                (start_date,),
            )
            admission_rows = cursor.fetchall()

            cursor.execute(
                f"""
                SELECT {discharge_expr} AS period_label, COUNT(*) AS total
                FROM [Admission]
                WHERE actual_discharge_date >= ?
                GROUP BY {discharge_expr}
                """,
                (start_date,),
            )
            discharge_rows = cursor.fetchall()

        merged = {}

        for row in admission_rows:
            label = str(row.period_label)
            merged.setdefault(label, {"admissions": 0, "discharges": 0})
            merged[label]["admissions"] = row.total

        for row in discharge_rows:
            label = str(row.period_label)
            merged.setdefault(label, {"admissions": 0, "discharges": 0})
            merged[label]["discharges"] = row.total

        return [
            AdmissionsAnalyticsItemSchema(
                label=label,
                admissions=data["admissions"],
                discharges=data["discharges"],
            )
            for label, data in sorted(merged.items())
        ]

    # ======================================================
    # Recent Activity Feed (AuditLog)
    # ======================================================

    @staticmethod
    @handle_db_errors("Failed to retrieve recent activity")
    def get_recent_activity(limit: int = 20) -> List[RecentActivityItemSchema]:

        with get_pyodbc_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT TOP (?)
                    al.audit_id,
                    al.table_name,
                    al.record_id,
                    al.action,
                    al.changed_by,
                    u.first_name AS changed_by_first_name,
                    u.last_name AS changed_by_last_name,
                    al.changed_at
                FROM [AuditLog] al
                LEFT JOIN [User] u ON al.changed_by = u.user_id
                ORDER BY al.changed_at DESC
                """,
                (limit,),
            )

            rows = cursor.fetchall()

        return [
            RecentActivityItemSchema(
                audit_id=row.audit_id,
                table_name=row.table_name,
                record_id=row.record_id,
                action=row.action,
                changed_by=row.changed_by,
                changed_by_name=(
                    f"{row.changed_by_first_name} {row.changed_by_last_name}"
                    if row.changed_by_first_name
                    else None
                ),
                changed_at=row.changed_at,
            )
            for row in rows
        ]
