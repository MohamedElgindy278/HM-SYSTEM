from typing import List

from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from src.schemas.doctor_schedule_schema import (
    DoctorScheduleCreateSchema,
    DoctorScheduleUpdateSchema,
    DoctorScheduleResponseSchema,
)


class DoctorScheduleService:
    @staticmethod
    def create_doctor_schedule(
        schedule_data: DoctorScheduleCreateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check doctor exists
                cursor.execute(
                    """

                            SELECT doctor_id
                            FROM [Doctor]
                            WHERE doctor_id = ?
                            """,
                    (schedule_data.doctor_id,),
                )

                if not cursor.fetchone():
                    raise Errors.doctor_not_found()

                # Check day of week is valid
                valid_days = [
                    "Saturday",
                    "Sunday",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ]

                if schedule_data.day_of_week not in valid_days:
                    raise Errors.invalid_day_of_week()

                # Check schedule time
                if schedule_data.start_time >= schedule_data.end_time:
                    raise Errors.invalid_schedule_time()

                # Check doctor already has schedule on this day
                cursor.execute(
                    """

                            SELECT schedule_id
                            FROM [DoctorSchedule]
                            WHERE doctor_id = ?
                            AND day_of_week = ?
                            """,
                    (
                        schedule_data.doctor_id,
                        schedule_data.day_of_week,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.doctor_schedule_exists()

                # Insert doctor schedule
                cursor.execute(
                    """

                            INSERT INTO [DoctorSchedule]
                            (
                                doctor_id,
                                day_of_week,
                                start_time,
                                end_time,
                                is_active
                            )
                            VALUES
                            (
                                ?, ?, ?, ?, ?
                            )
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

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create doctor schedule",
            )

    @staticmethod
    def update_doctor_schedule(
        schedule_id: int,
        schedule_data: DoctorScheduleUpdateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check schedule exists
                cursor.execute(
                    """

                    SELECT
                        doctor_id
                    FROM [DoctorSchedule]
                    WHERE schedule_id = ?
                    """,
                    (schedule_id,),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.doctor_schedule_not_found()

                doctor_id = row.doctor_id

                # Check day of week is valid
                valid_days = [
                    "Saturday",
                    "Sunday",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ]

                if schedule_data.day_of_week not in valid_days:
                    raise Errors.invalid_day_of_week()

                # Check schedule time
                if schedule_data.start_time >= schedule_data.end_time:
                    raise Errors.invalid_schedule_time()

                # Check doctor already has schedule on this day
                cursor.execute(
                    """

                    SELECT schedule_id
                    FROM [DoctorSchedule]
                    WHERE doctor_id = ?
                    AND day_of_week = ?
                    AND schedule_id <> ?
                    """,
                    (
                        doctor_id,
                        schedule_data.day_of_week,
                        schedule_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.doctor_schedule_exists()

                # Update schedule
                cursor.execute(
                    """

                    UPDATE [DoctorSchedule]
                    SET
                        day_of_week = ?,
                        start_time = ?,
                        end_time = ?,
                        is_active = ?
                    WHERE schedule_id = ?
                    """,
                    (
                        schedule_data.day_of_week,
                        schedule_data.start_time,
                        schedule_data.end_time,
                        schedule_data.is_active,
                        schedule_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update doctor schedule",
            )

    @staticmethod
    def get_doctor_schedule_by_id(
        schedule_id: int,
    ) -> DoctorScheduleResponseSchema:

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT
                        schedule_id,
                        doctor_id,
                        day_of_week,
                        start_time,
                        end_time,
                        is_active
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
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve doctor schedule",
            )

    @staticmethod
    def get_all_doctor_schedules() -> List[DoctorScheduleResponseSchema]:

        schedules = []

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT
                        schedule_id,
                        doctor_id,
                        day_of_week,
                        start_time,
                        end_time,
                        is_active
                    FROM [DoctorSchedule]
                    """,
                )

                rows = cursor.fetchall()

                for row in rows:

                    schedules.append(
                        DoctorScheduleResponseSchema(
                            schedule_id=row.schedule_id,
                            doctor_id=row.doctor_id,
                            day_of_week=row.day_of_week,
                            start_time=row.start_time,
                            end_time=row.end_time,
                            is_active=row.is_active,
                        )
                    )

                return schedules

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve doctor schedules",
            )
