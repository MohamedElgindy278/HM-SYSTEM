from datetime import date, datetime, time, timedelta
from typing import List, Optional

from pyodbc import IntegrityError

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.appointment_schema import (
    AppointmentCreateSchema,
    AppointmentResponseSchema,
    AppointmentUpdateSchema,
)
from src.schemas.common_schema import PaginatedResponse
from src.core.query_utils import build_where_clause, paginate


class AppointmentService:

    @staticmethod
    def _generate_time_slots(
        start_time: time,
        end_time: time,
        appointment_duration: int,
    ) -> List[time]:

        slots = []
        reference_day = date.today()

        current_time = datetime.combine(reference_day, start_time)
        shift_end = datetime.combine(reference_day, end_time)

        while current_time + timedelta(minutes=appointment_duration) <= shift_end:
            slots.append(current_time.time())
            current_time += timedelta(minutes=appointment_duration)

        return slots

    @staticmethod
    @handle_db_errors("Failed to retrieve available slots")
    def get_available_slots(
        doctor_id: int,
        appointment_date: date,
        exclude_appointment_id: Optional[int] = None,
    ) -> List[time]:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT d.is_active, s.appointment_duration
                FROM [Doctor] d
                INNER JOIN [Specialty] s ON d.specialty_id = s.specialty_id
                WHERE d.doctor_id = ?
                """,
                (doctor_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.doctor_not_found()

            if not row.is_active:
                raise Errors.doctor_not_available()

            appointment_duration = row.appointment_duration
            day_of_week = appointment_date.strftime("%A")

            cursor.execute(
                """
                SELECT start_time, end_time
                FROM [DoctorSchedule]
                WHERE doctor_id = ?
                AND day_of_week = ?
                AND is_active = 1
                """,
                (doctor_id, day_of_week),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.doctor_not_available()

            slots = AppointmentService._generate_time_slots(
                start_time=row.start_time,
                end_time=row.end_time,
                appointment_duration=appointment_duration,
            )

            # Exclude the appointment being rescheduled so it can't block itself
            if exclude_appointment_id is not None:
                cursor.execute(
                    """
                    SELECT appointment_date
                    FROM [Appointment]
                    WHERE doctor_id = ?
                    AND CAST(appointment_date AS DATE) = ?
                    AND status = 'Scheduled'
                    AND appointment_id <> ?
                    """,
                    (doctor_id, appointment_date, exclude_appointment_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT appointment_date
                    FROM [Appointment]
                    WHERE doctor_id = ?
                    AND CAST(appointment_date AS DATE) = ?
                    AND status = 'Scheduled'
                    """,
                    (doctor_id, appointment_date),
                )

            reserved_slots = {r.appointment_date.time() for r in cursor.fetchall()}

            return [slot for slot in slots if slot not in reserved_slots]

    @staticmethod
    @handle_db_errors("Failed to create appointment")
    def create_appointment(appointment_data: AppointmentCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT patient_id FROM [Patient] WHERE patient_id = ? AND is_deleted = 0",
                (appointment_data.patient_id,),
            )
            if not cursor.fetchone():
                raise Errors.patient_not_found()

            # Doctor must exist AND have a clinic assigned - that clinic
            # becomes the appointment's clinic_id snapshot automatically.
            cursor.execute(
                """
                SELECT d.clinic_id, c.is_active AS clinic_is_active
                FROM [Doctor] d
                LEFT JOIN [Clinic] c ON d.clinic_id = c.clinic_id
                WHERE d.doctor_id = ?
                """,
                (appointment_data.doctor_id,),
            )
            doctor_row = cursor.fetchone()

            if not doctor_row:
                raise Errors.doctor_not_found()

            if doctor_row.clinic_id is None:
                raise Errors.validation_error(
                    "This doctor has no clinic assigned yet",
                )

            if not doctor_row.clinic_is_active:
                raise Errors.validation_error(
                    "This doctor's assigned clinic is not active",
                )

            clinic_id = doctor_row.clinic_id

            if appointment_data.appointment_date <= datetime.now():
                raise Errors.invalid_appointment_date()

            available_slots = AppointmentService.get_available_slots(
                appointment_data.doctor_id,
                appointment_data.appointment_date.date(),
            )

            if appointment_data.appointment_date.time() not in available_slots:
                raise Errors.doctor_not_available()

            cursor.execute(
                """
                SELECT appointment_id
                FROM [Appointment]
                WHERE patient_id = ?
                AND appointment_date = ?
                AND status = 'Scheduled'
                """,
                (appointment_data.patient_id, appointment_data.appointment_date),
            )
            if cursor.fetchone():
                raise Errors.patient_has_appointment()

            try:
                cursor.execute(
                    """
                    INSERT INTO [Appointment]
                    (patient_id, doctor_id, clinic_id, appointment_date, status, notes)
                    VALUES (?, ?, ?, ?, 'Scheduled', ?)
                    """,
                    (
                        appointment_data.patient_id,
                        appointment_data.doctor_id,
                        clinic_id,
                        appointment_data.appointment_date,
                        appointment_data.notes,
                    ),
                )
                conn.commit()

            except IntegrityError as e:
                if "UQ_Appointment_DoctorSlot" in str(e):
                    raise Errors.doctor_not_available()
                if "UQ_Appointment_PatientSlot" in str(e):
                    raise Errors.patient_has_appointment()
                raise

    @staticmethod
    @handle_db_errors("Failed to update appointment")
    def update_appointment(
        appointment_id: int, appointment_data: AppointmentUpdateSchema
    ) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT patient_id, doctor_id, clinic_id, appointment_date, status, notes
                FROM [Appointment]
                WHERE appointment_id = ?
                """,
                (appointment_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.appointment_not_found()

            fields = appointment_data.model_dump(exclude_unset=True)

            doctor_id = fields.get("doctor_id", row.doctor_id)
            appointment_date = fields.get("appointment_date", row.appointment_date)
            notes = fields.get("notes", row.notes)

            doctor_or_time_changed = (
                doctor_id != row.doctor_id or appointment_date != row.appointment_date
            )

            if row.status != "Scheduled" and doctor_or_time_changed:
                raise Errors.validation_error(
                    "Cannot reschedule a completed or cancelled appointment",
                )

            # clinic_id stays untouched unless the doctor actually changes
            clinic_id = row.clinic_id

            if doctor_id != row.doctor_id:
                cursor.execute(
                    """
                    SELECT d.clinic_id, c.is_active AS clinic_is_active
                    FROM [Doctor] d
                    LEFT JOIN [Clinic] c ON d.clinic_id = c.clinic_id
                    WHERE d.doctor_id = ?
                    """,
                    (doctor_id,),
                )
                doctor_row = cursor.fetchone()

                if not doctor_row:
                    raise Errors.doctor_not_found()

                if doctor_row.clinic_id is None:
                    raise Errors.validation_error(
                        "This doctor has no clinic assigned yet",
                    )

                if not doctor_row.clinic_is_active:
                    raise Errors.validation_error(
                        "This doctor's assigned clinic is not active",
                    )

                clinic_id = (
                    doctor_row.clinic_id
                )  # re-snapshot to the new doctor's clinic

            if doctor_or_time_changed:
                if appointment_date <= datetime.now():
                    raise Errors.invalid_appointment_date()

                available_slots = AppointmentService.get_available_slots(
                    doctor_id,
                    appointment_date.date(),
                    exclude_appointment_id=appointment_id,
                )
                if appointment_date.time() not in available_slots:
                    raise Errors.doctor_not_available()

                cursor.execute(
                    """
                    SELECT appointment_id
                    FROM [Appointment]
                    WHERE patient_id = ?
                    AND appointment_date = ?
                    AND status = 'Scheduled'
                    AND appointment_id <> ?
                    """,
                    (row.patient_id, appointment_date, appointment_id),
                )
                if cursor.fetchone():
                    raise Errors.patient_has_appointment()

            try:
                cursor.execute(
                    """
                    UPDATE [Appointment]
                    SET doctor_id = ?, clinic_id = ?, appointment_date = ?, notes = ?, updated_at = GETDATE()
                    WHERE appointment_id = ?
                    """,
                    (doctor_id, clinic_id, appointment_date, notes, appointment_id),
                )
                conn.commit()
            except IntegrityError as e:
                if "UQ_Appointment_DoctorSlot" in str(e):
                    raise Errors.doctor_not_available()
                if "UQ_Appointment_PatientSlot" in str(e):
                    raise Errors.patient_has_appointment()
                raise

    @staticmethod
    @handle_db_errors("Failed to retrieve appointment")
    def get_appointment_by_id(appointment_id: int) -> AppointmentResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT appointment_id, patient_id, doctor_id, clinic_id, appointment_date,
                       status, notes, created_at, updated_at
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
                clinic_id=row.clinic_id,
                appointment_date=row.appointment_date,
                status=row.status,
                notes=row.notes,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve appointments")
    def get_all_appointments(
        start_num: int = 1,
        page_size: int = 20,
        doctor_id: Optional[int] = None,
        patient_id: Optional[int] = None,
        status: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> PaginatedResponse[AppointmentResponseSchema]:

        where_clause, params = build_where_clause(
            [
                ("doctor_id = ?", doctor_id),
                ("patient_id = ?", patient_id),
                ("status = ?", status),
                ("CAST(appointment_date AS DATE) >= ?", from_date),
                ("CAST(appointment_date AS DATE) <= ?", to_date),
            ]
        )

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT COUNT(*) AS total FROM [Appointment] {where_clause}", params
            )
            total = cursor.fetchone().total

            cursor.execute(
                f"""
                SELECT appointment_id, patient_id, doctor_id, clinic_id, appointment_date,
                    status, notes, created_at, updated_at
                FROM [Appointment]
                {where_clause}
                ORDER BY appointment_date
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                params + [offset, limit],
            )
            rows = cursor.fetchall()

            items = [
                AppointmentResponseSchema(
                    appointment_id=row.appointment_id,
                    patient_id=row.patient_id,
                    doctor_id=row.doctor_id,
                    clinic_id=row.clinic_id,
                    appointment_date=row.appointment_date,
                    status=row.status,
                    notes=row.notes,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]

            return PaginatedResponse(items=items, total=total)

    @staticmethod
    @handle_db_errors("Failed to cancel appointment")
    def cancel_appointment(appointment_id: int) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT status FROM [Appointment] WHERE appointment_id = ?",
                (appointment_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.appointment_not_found()

            if row.status != "Scheduled":
                raise Errors.validation_error(
                    "Only scheduled appointments can be cancelled"
                )

            cursor.execute(
                "UPDATE [Appointment] SET status = 'Cancelled', updated_at = GETDATE() WHERE appointment_id = ?",
                (appointment_id,),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to complete appointment")
    def complete_appointment(appointment_id: int) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT status FROM [Appointment] WHERE appointment_id = ?",
                (appointment_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.appointment_not_found()

            if row.status != "Scheduled":
                raise Errors.validation_error(
                    "Only scheduled appointments can be completed"
                )

            cursor.execute(
                "UPDATE [Appointment] SET status = 'Completed', updated_at = GETDATE() WHERE appointment_id = ?",
                (appointment_id,),
            )
            conn.commit()
