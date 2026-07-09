from typing import List

from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from src.schemas.appointment_schema import (
    AppointmentCreateSchema,
    AppointmentResponseSchema,
    AppointmentUpdateSchema,
)
from datetime import (
    date,
    time,
    datetime,
    timedelta,
)


class AppointmentService:
    @staticmethod
    def _generate_time_slots(
        start_time: time,
        end_time: time,
        appointment_duration: int,
    ) -> list[time]:

        slots = []

        current_time = datetime.combine(
            datetime.today(),
            start_time,
        )

        shift_end = datetime.combine(
            datetime.today(),
            end_time,
        )

        while (
            current_time
            + timedelta(
                minutes=appointment_duration,
            )
            <= shift_end
        ):

            slots.append(
                current_time.time(),
            )

            current_time += timedelta(
                minutes=appointment_duration,
            )

        return slots

    @staticmethod
    def get_available_slots(
        doctor_id: int,
        appointment_date: date,
    ):

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check doctor exists and get appointment duration
                cursor.execute(
                    """

                        SELECT
                            s.appointment_duration
                        FROM [Doctor] d
                        INNER JOIN [Specialty] s
                            ON d.specialty_id = s.specialty_id
                        WHERE d.doctor_id = ?

                        """,
                    (doctor_id,),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.doctor_not_found()

                appointment_duration = row.appointment_duration

                # Get requested day name
                day_of_week = appointment_date.strftime(
                    "%A",
                )

                # Get doctor schedule
                cursor.execute(
                    """

                        SELECT
                            start_time,
                            end_time
                        FROM [DoctorSchedule]
                        WHERE doctor_id = ?
                        AND day_of_week = ?
                        AND is_active = 1

                        """,
                    (
                        doctor_id,
                        day_of_week,
                    ),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.doctor_not_available()

                start_time = row.start_time
                end_time = row.end_time

                # Generate all available time slots
                slots = AppointmentService._generate_time_slots(
                    start_time=start_time,
                    end_time=end_time,
                    appointment_duration=appointment_duration,
                )

                # Get reserved appointments
                cursor.execute(
                    """

                        SELECT
                            appointment_date
                        FROM [Appointment]
                        WHERE doctor_id = ?
                        AND CAST(appointment_date AS DATE) = ?
                        AND status = ?

                        """,
                    (
                        doctor_id,
                        appointment_date,
                        "Scheduled",
                    ),
                )

                rows = cursor.fetchall()

                reserved_slots = [row.appointment_date.time() for row in rows]

                # Remove reserved slots
                available_slots = [slot for slot in slots if slot not in reserved_slots]

                return available_slots

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve available slots",
            )

    @staticmethod
    def create_appointment(
        appointment_data: AppointmentCreateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check patient exists
                cursor.execute(
                    """
                    SELECT patient_id
                    FROM [Patient]
                    WHERE patient_id = ?
                    """,
                    (appointment_data.patient_id,),
                )

                if not cursor.fetchone():
                    raise Errors.patient_not_found()

                # Check doctor exists
                cursor.execute(
                    """
                    SELECT doctor_id
                    FROM [Doctor]
                    WHERE doctor_id = ?
                    """,
                    (appointment_data.doctor_id,),
                )

                if not cursor.fetchone():
                    raise Errors.doctor_not_found()

                # Check appointment date is valid
                if appointment_data.appointment_date <= datetime.now():
                    raise Errors.invalid_appointment_date()

                # Get available slots
                available_slots = AppointmentService.get_available_slots(
                    appointment_data.doctor_id,
                    appointment_data.appointment_date.date(),
                )

                appointment_time = appointment_data.appointment_date.time()

                # Check selected slot is available
                if appointment_time not in available_slots:
                    raise Errors.doctor_not_available()

                # Check patient already has appointment
                cursor.execute(
                    """
                    SELECT appointment_id
                    FROM [Appointment]
                    WHERE patient_id = ?
                    AND appointment_date = ?
                    AND status = ?
                    """,
                    (
                        appointment_data.patient_id,
                        appointment_data.appointment_date,
                        "Scheduled",
                    ),
                )

                if cursor.fetchone():
                    raise Errors.patient_has_appointment()

                # Insert appointment
                cursor.execute(
                    """
                    INSERT INTO [Appointment]
                    (
                        patient_id,
                        doctor_id,
                        appointment_date,
                        status,
                        notes
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        appointment_data.patient_id,
                        appointment_data.doctor_id,
                        appointment_data.appointment_date,
                        appointment_data.status,
                        appointment_data.notes,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create appointment",
            )

    @staticmethod
    def update_appointment(
        appointment_id: int,
        appointment_data: AppointmentUpdateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check appointment exists
                cursor.execute(
                    """
                    SELECT
                        patient_id,
                        doctor_id,
                        appointment_date,
                        status,
                        notes
                    FROM [Appointment]
                    WHERE appointment_id = ?
                    """,
                    (appointment_id,),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.appointment_not_found()

                # Merge old values with new values
                patient_id = row.patient_id

                doctor_id = (
                    appointment_data.doctor_id
                    if appointment_data.doctor_id is not None
                    else row.doctor_id
                )

                appointment_date = (
                    appointment_data.appointment_date
                    if appointment_data.appointment_date is not None
                    else row.appointment_date
                )

                status = (
                    appointment_data.status
                    if appointment_data.status is not None
                    else row.status
                )

                notes = (
                    appointment_data.notes
                    if appointment_data.notes is not None
                    else row.notes
                )

                # Check doctor exists
                cursor.execute(
                    """
                    SELECT doctor_id
                    FROM [Doctor]
                    WHERE doctor_id = ?
                    """,
                    (doctor_id,),
                )

                if not cursor.fetchone():
                    raise Errors.doctor_not_found()

                # Check appointment date is valid
                if appointment_date <= datetime.now():
                    raise Errors.invalid_appointment_date()

                # Get available slots
                available_slots = AppointmentService.get_available_slots(
                    doctor_id,
                    appointment_date.date(),
                )

                appointment_time = appointment_date.time()
                current_time = row.appointment_date.time()

                # Check doctor availability
                if (
                    appointment_time != current_time
                    and appointment_time not in available_slots
                ):
                    raise Errors.doctor_not_available()

                # Check patient doesn't have another appointment
                cursor.execute(
                    """
                    SELECT appointment_id
                    FROM [Appointment]
                    WHERE patient_id = ?
                    AND appointment_date = ?
                    AND status = ?
                    AND appointment_id <> ?
                    """,
                    (
                        patient_id,
                        appointment_date,
                        "Scheduled",
                        appointment_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.patient_has_appointment()

                # Update appointment
                cursor.execute(
                    """
                    UPDATE [Appointment]
                    SET
                        doctor_id = ?,
                        appointment_date = ?,
                        status = ?,
                        notes = ?
                    WHERE appointment_id = ?
                    """,
                    (
                        doctor_id,
                        appointment_date,
                        status,
                        notes,
                        appointment_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update appointment",
            )

    @staticmethod
    def get_appointment_by_id(
        appointment_id: int,
    ) -> AppointmentResponseSchema:

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT
                        appointment_id,
                        patient_id,
                        doctor_id,
                        appointment_date,
                        status,
                        notes,
                        created_at
                    FROM [Appointment]
                    WHERE appointment_id = ?
                    """,
                    (appointment_id,),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.appointment_not_found()

                return AppointmentResponseSchema(
                    appointment_id=row.appointment_id,
                    patient_id=row.patient_id,
                    doctor_id=row.doctor_id,
                    appointment_date=row.appointment_date,
                    status=row.status,
                    notes=row.notes,
                    created_at=row.created_at,
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve appointment",
            )

    @staticmethod
    def get_all_appointments() -> list[AppointmentResponseSchema]:

        appointments = []

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute("""
                    SELECT
                        appointment_id,
                        patient_id,
                        doctor_id,
                        appointment_date,
                        status,
                        notes,
                        created_at
                    FROM [Appointment]
                    ORDER BY appointment_date
                    """)

                rows = cursor.fetchall()

                for row in rows:

                    appointments.append(
                        AppointmentResponseSchema(
                            appointment_id=row.appointment_id,
                            patient_id=row.patient_id,
                            doctor_id=row.doctor_id,
                            appointment_date=row.appointment_date,
                            status=row.status,
                            notes=row.notes,
                            created_at=row.created_at,
                        )
                    )

                return appointments

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve appointments",
            )

    @staticmethod
    def cancel_appointment(
        appointment_id: int,
    ):

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT appointment_id
                    FROM [Appointment]
                    WHERE appointment_id = ?
                    """,
                    (appointment_id,),
                )

                if not cursor.fetchone():
                    raise Errors.appointment_not_found()

                cursor.execute(
                    """
                    UPDATE [Appointment]
                    SET status = ?
                    WHERE appointment_id = ?
                    """,
                    (
                        "Cancelled",
                        appointment_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to cancel appointment",
            )

    @staticmethod
    def complete_appointment(
        appointment_id: int,
    ):

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT appointment_id
                    FROM [Appointment]
                    WHERE appointment_id = ?
                    """,
                    (appointment_id,),
                )

                if not cursor.fetchone():
                    raise Errors.appointment_not_found()

                cursor.execute(
                    """
                    UPDATE [Appointment]
                    SET status = ?
                    WHERE appointment_id = ?
                    """,
                    (
                        "Completed",
                        appointment_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to complete appointment",
            )
