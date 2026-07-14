from typing import List, Optional

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.auth_schema import CurrentUserSchema
from src.schemas.doctor_schedule_schema import (
    DoctorScheduleCreateSchema,
    DoctorScheduleResponseSchema,
    DoctorScheduleUpdateSchema,
)


class DoctorScheduleService:

    @staticmethod
    @handle_db_errors("Failed to create doctor schedule")
    def create_doctor_schedule(schedule_data: DoctorScheduleCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT doctor_id FROM [Doctor] WHERE doctor_id = ?",
                (schedule_data.doctor_id,),
            )
            if not cursor.fetchone():
                raise Errors.doctor_not_found()

            cursor.execute(
                "SELECT schedule_id FROM [DoctorSchedule] WHERE doctor_id = ? AND day_of_week = ?",
                (schedule_data.doctor_id, schedule_data.day_of_week),
            )
            if cursor.fetchone():
                raise Errors.doctor_schedule_exists()

            cursor.execute(
                """
                INSERT INTO [DoctorSchedule]
                (doctor_id, day_of_week, start_time, end_time, is_active)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    schedule_data.doctor_id,
                    schedule_data.day_of_week,
                    schedule_data.start_time,
                    schedule_data.end_time,
                    schedule_data.is_active,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to update doctor schedule")
    def update_doctor_schedule(
        schedule_id: int,
        schedule_data: DoctorScheduleUpdateSchema,
        current_user: CurrentUserSchema,
    ) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Fetch current row + the schedule's owning doctor's user_id
            cursor.execute(
                """
                SELECT ds.doctor_id, ds.day_of_week, ds.start_time, ds.end_time, ds.is_active,
                       d.user_id AS doctor_user_id
                FROM [DoctorSchedule] ds
                INNER JOIN [Doctor] d ON ds.doctor_id = d.doctor_id
                WHERE ds.schedule_id = ?
                """,
                (schedule_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.doctor_schedule_not_found()

            # Admins can update any schedule; everyone else must own it
            if (
                "Admin" not in current_user.roles
                and row.doctor_user_id != current_user.user_id
            ):
                raise Errors.forbidden()

            fields = schedule_data.model_dump(exclude_unset=True)

            day_of_week = fields.get("day_of_week", row.day_of_week)
            start_time = fields.get("start_time", row.start_time)
            end_time = fields.get("end_time", row.end_time)
            is_active = fields.get("is_active", row.is_active)

            if start_time >= end_time:
                raise Errors.invalid_schedule_time()

            if day_of_week != row.day_of_week:
                cursor.execute(
                    """
                    SELECT schedule_id FROM [DoctorSchedule]
                    WHERE doctor_id = ? AND day_of_week = ? AND schedule_id <> ?
                    """,
                    (row.doctor_id, day_of_week, schedule_id),
                )
                if cursor.fetchone():
                    raise Errors.doctor_schedule_exists()

            cursor.execute(
                """
                UPDATE [DoctorSchedule]
                SET
                    day_of_week = ?, start_time = ?, end_time = ?,
                    is_active = ?, updated_at = GETDATE()
                WHERE schedule_id = ?
                """,
                (day_of_week, start_time, end_time, is_active, schedule_id),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve doctor schedule")
    def get_doctor_schedule_by_id(schedule_id: int) -> DoctorScheduleResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    schedule_id, doctor_id, day_of_week, start_time, end_time, is_active,
                    created_at, updated_at
                FROM [DoctorSchedule]
                WHERE schedule_id = ?
                """,
                (schedule_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.doctor_schedule_not_found()

            return DoctorScheduleResponseSchema(
                schedule_id=row.schedule_id,
                doctor_id=row.doctor_id,
                day_of_week=row.day_of_week,
                start_time=row.start_time,
                end_time=row.end_time,
                is_active=row.is_active,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve doctor schedules")
    def get_all_doctor_schedules(
        doctor_id: Optional[int] = None,
    ) -> List[DoctorScheduleResponseSchema]:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            day_order = """
                CASE day_of_week
                    WHEN 'Saturday' THEN 1 WHEN 'Sunday' THEN 2 WHEN 'Monday' THEN 3
                    WHEN 'Tuesday' THEN 4 WHEN 'Wednesday' THEN 5 WHEN 'Thursday' THEN 6
                    WHEN 'Friday' THEN 7
                END
            """

            if doctor_id is not None:
                cursor.execute(
                    f"""
                    SELECT
                        schedule_id, doctor_id, day_of_week, start_time, end_time, is_active,
                        created_at, updated_at
                    FROM [DoctorSchedule]
                    WHERE doctor_id = ?
                    ORDER BY {day_order}
                    """,
                    (doctor_id,),
                )
            else:
                cursor.execute(f"""
                    SELECT
                        schedule_id, doctor_id, day_of_week, start_time, end_time, is_active,
                        created_at, updated_at
                    FROM [DoctorSchedule]
                    ORDER BY doctor_id, {day_order}
                    """)

            rows = cursor.fetchall()

            return [
                DoctorScheduleResponseSchema(
                    schedule_id=row.schedule_id,
                    doctor_id=row.doctor_id,
                    day_of_week=row.day_of_week,
                    start_time=row.start_time,
                    end_time=row.end_time,
                    is_active=row.is_active,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]
