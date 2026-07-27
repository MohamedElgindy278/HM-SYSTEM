from typing import List, Optional

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.patient_queue_schema import (
    PatientQueueCheckInSchema,
    PatientQueueEmergencyCheckInSchema,
    PatientQueueResponseSchema,
)


class PatientQueueService:

    @staticmethod
    @handle_db_errors("Failed to check in patient")
    def check_in(check_in_data: PatientQueueCheckInSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT patient_id, clinic_id, status
                FROM [Appointment]
                WHERE appointment_id = ?
                """,
                (check_in_data.appointment_id,),
            )
            appointment = cursor.fetchone()

            if not appointment:
                raise Errors.appointment_not_found()

            if appointment.status != "Scheduled":
                raise Errors.validation_error(
                    "Only scheduled appointments can be checked in",
                )

            if appointment.clinic_id is None:
                raise Errors.validation_error(
                    "This appointment has no clinic assigned",
                )

            cursor.execute(
                """
                SELECT queue_id
                FROM [PatientQueue]
                WHERE appointment_id = ?
                AND status IN ('Waiting', 'InProgress')
                """,
                (check_in_data.appointment_id,),
            )
            if cursor.fetchone():
                raise Errors.validation_error(
                    "This appointment is already checked in",
                )

            cursor.execute(
                """
                INSERT INTO [PatientQueue]
                (patient_id, clinic_id, appointment_id, status)
                VALUES (?, ?, ?, 'Waiting')
                """,
                (
                    appointment.patient_id,
                    appointment.clinic_id,
                    check_in_data.appointment_id,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to check in emergency patient")
    def emergency_check_in(data: PatientQueueEmergencyCheckInSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT patient_id FROM [Patient] WHERE patient_id = ? AND is_deleted = 0",
                (data.patient_id,),
            )
            if not cursor.fetchone():
                raise Errors.patient_not_found()

            cursor.execute(
                """
                SELECT c.clinic_id
                FROM [Clinic] c
                INNER JOIN [Department] d ON c.department_id = d.department_id
                WHERE c.clinic_id = ? AND c.is_active = 1 AND d.is_emergency = 1
                """,
                (data.clinic_id,),
            )
            if not cursor.fetchone():
                raise Errors.validation_error(
                    "Clinic not found or is not an emergency clinic",
                )

            cursor.execute(
                """
                INSERT INTO [PatientQueue]
                (patient_id, clinic_id, appointment_id, status)
                VALUES (?, ?, NULL, 'Waiting')
                """,
                (data.patient_id, data.clinic_id),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to call patient")
    def call_patient(queue_id: int) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT status FROM [PatientQueue] WHERE queue_id = ?",
                (queue_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.queue_entry_not_found()

            if row.status != "Waiting":
                raise Errors.validation_error(
                    "Only patients currently waiting can be called",
                )

            cursor.execute(
                """
                UPDATE [PatientQueue]
                SET status = 'InProgress', called_time = GETDATE()
                WHERE queue_id = ?
                """,
                (queue_id,),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to mark patient as no-show")
    def mark_no_show(queue_id: int) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT status FROM [PatientQueue] WHERE queue_id = ?",
                (queue_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.queue_entry_not_found()

            if row.status != "Waiting":
                raise Errors.validation_error(
                    "Only patients currently waiting can be marked as no-show",
                )

            cursor.execute(
                "UPDATE [PatientQueue] SET status = 'NoShow' WHERE queue_id = ?",
                (queue_id,),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve queue")
    def get_clinic_queue(
        clinic_id: int,
        status: Optional[str] = None,
    ) -> List[PatientQueueResponseSchema]:

        params = [clinic_id]
        status_filter = ""

        if status:
            status_filter = "AND status = ?"
            params.append(status)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"""
                SELECT queue_id, patient_id, clinic_id, appointment_id,
                       check_in_time, called_time, status
                FROM [PatientQueue]
                WHERE clinic_id = ?
                AND CAST(check_in_time AS DATE) = CAST(GETDATE() AS DATE)
                {status_filter}
                ORDER BY check_in_time
                """,
                params,
            )
            rows = cursor.fetchall()

            return [
                PatientQueueResponseSchema(
                    queue_id=row.queue_id,
                    patient_id=row.patient_id,
                    clinic_id=row.clinic_id,
                    appointment_id=row.appointment_id,
                    check_in_time=row.check_in_time,
                    called_time=row.called_time,
                    status=row.status,
                )
                for row in rows
            ]
