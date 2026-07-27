from typing import Optional

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.common_schema import PaginatedResponse
from src.schemas.doctor_schema import (
    DoctorCreateSchema,
    DoctorResponseSchema,
    DoctorUpdateSchema,
)
from src.core.query_utils import build_where_clause, paginate


class DoctorService:

    @staticmethod
    def _check_clinic_exists_and_active(cursor, clinic_id: int) -> None:
        cursor.execute(
            "SELECT clinic_id FROM [Clinic] WHERE clinic_id = ? AND is_active = 1",
            (clinic_id,),
        )
        if not cursor.fetchone():
            raise Errors.clinic_not_found()

    @staticmethod
    @handle_db_errors("Failed to create doctor")
    def create_doctor(doctor_data: DoctorCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check user exists
            cursor.execute(
                "SELECT user_id FROM [User] WHERE user_id = ? AND is_deleted = 0",
                (doctor_data.user_id,),
            )
            if not cursor.fetchone():
                raise Errors.user_not_found()

            # Check specialty exists
            cursor.execute(
                "SELECT specialty_id FROM [Specialty] WHERE specialty_id = ?",
                (doctor_data.specialty_id,),
            )
            if not cursor.fetchone():
                raise Errors.specialty_not_found()

            # Check branch exists
            cursor.execute(
                "SELECT branch_id FROM [Branch] WHERE branch_id = ?",
                (doctor_data.branch_id,),
            )
            if not cursor.fetchone():
                raise Errors.branch_not_found()

            # Check clinic exists and is active (only if one was provided)
            if doctor_data.clinic_id is not None:
                DoctorService._check_clinic_exists_and_active(
                    cursor, doctor_data.clinic_id
                )

            # Check user isn't already a doctor
            cursor.execute(
                "SELECT doctor_id FROM [Doctor] WHERE user_id = ?",
                (doctor_data.user_id,),
            )
            if cursor.fetchone():
                raise Errors.doctor_exists()

            # Check license number
            cursor.execute(
                "SELECT doctor_id FROM [Doctor] WHERE license_number = ?",
                (doctor_data.license_number,),
            )
            if cursor.fetchone():
                raise Errors.doctor_license_exists()

            cursor.execute(
                """
                INSERT INTO [Doctor]
                (user_id, specialty_id, branch_id, clinic_id, license_number, years_of_experience)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    doctor_data.user_id,
                    doctor_data.specialty_id,
                    doctor_data.branch_id,
                    doctor_data.clinic_id,
                    doctor_data.license_number,
                    doctor_data.years_of_experience,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to update doctor")
    def update_doctor(doctor_id: int, doctor_data: DoctorUpdateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Fetch current row
            cursor.execute(
                """
                SELECT specialty_id, branch_id, clinic_id, license_number,
                       years_of_experience, is_active
                FROM [Doctor]
                WHERE doctor_id = ?
                """,
                (doctor_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.doctor_not_found()

            # Merge sent fields with current values
            fields = doctor_data.model_dump(exclude_unset=True)

            specialty_id = fields.get("specialty_id", row.specialty_id)
            branch_id = fields.get("branch_id", row.branch_id)
            clinic_id = fields.get("clinic_id", row.clinic_id)
            license_number = fields.get("license_number", row.license_number)
            years_of_experience = fields.get(
                "years_of_experience", row.years_of_experience
            )
            is_active = fields.get("is_active", row.is_active)

            # Check specialty exists only if it changed
            if specialty_id != row.specialty_id:
                cursor.execute(
                    "SELECT specialty_id FROM [Specialty] WHERE specialty_id = ?",
                    (specialty_id,),
                )
                if not cursor.fetchone():
                    raise Errors.specialty_not_found()

            # Check branch exists only if it changed
            if branch_id != row.branch_id:
                cursor.execute(
                    "SELECT branch_id FROM [Branch] WHERE branch_id = ?",
                    (branch_id,),
                )
                if not cursor.fetchone():
                    raise Errors.branch_not_found()

            # Check clinic exists and is active only if it changed to a
            # non-null value. Setting clinic_id explicitly to null
            # (unassigning the doctor) needs no lookup.
            if clinic_id != row.clinic_id and clinic_id is not None:
                DoctorService._check_clinic_exists_and_active(cursor, clinic_id)

            # Check license number uniqueness only if it changed
            if license_number != row.license_number:
                cursor.execute(
                    "SELECT doctor_id FROM [Doctor] WHERE license_number = ? AND doctor_id <> ?",
                    (license_number, doctor_id),
                )
                if cursor.fetchone():
                    raise Errors.doctor_license_exists()

            cursor.execute(
                """
                UPDATE [Doctor]
                SET
                    specialty_id = ?, branch_id = ?, clinic_id = ?, license_number = ?,
                    years_of_experience = ?, is_active = ?, updated_at = GETDATE()
                WHERE doctor_id = ?
                """,
                (
                    specialty_id,
                    branch_id,
                    clinic_id,
                    license_number,
                    years_of_experience,
                    is_active,
                    doctor_id,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve doctor")
    def get_doctor_by_id(doctor_id: int) -> DoctorResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    doctor_id, user_id, specialty_id, branch_id, clinic_id,
                    license_number, years_of_experience, is_active,
                    created_at, updated_at
                FROM [Doctor]
                WHERE doctor_id = ?
                """,
                (doctor_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.doctor_not_found()

            return DoctorResponseSchema(
                doctor_id=row.doctor_id,
                user_id=row.user_id,
                specialty_id=row.specialty_id,
                branch_id=row.branch_id,
                clinic_id=row.clinic_id,
                license_number=row.license_number,
                years_of_experience=row.years_of_experience,
                is_active=row.is_active,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve doctors")
    def get_all_doctors(
        start_num: int = 1,
        page_size: int = 20,
        specialty_id: Optional[int] = None,
        branch_id: Optional[int] = None,
        clinic_id: Optional[int] = None,
    ) -> PaginatedResponse[DoctorResponseSchema]:

        where_clause, params = build_where_clause(
            [
                ("specialty_id = ?", specialty_id),
                ("branch_id = ?", branch_id),
                ("clinic_id = ?", clinic_id),
            ]
        )

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT COUNT(*) AS total FROM [Doctor] {where_clause}", params
            )
            total = cursor.fetchone().total

            cursor.execute(
                f"""
                SELECT
                    doctor_id, user_id, specialty_id, branch_id, clinic_id,
                    license_number, years_of_experience, is_active,
                    created_at, updated_at
                FROM [Doctor]
                {where_clause}
                ORDER BY doctor_id
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                params + [offset, limit],
            )
            rows = cursor.fetchall()

            items = [
                DoctorResponseSchema(
                    doctor_id=row.doctor_id,
                    user_id=row.user_id,
                    specialty_id=row.specialty_id,
                    branch_id=row.branch_id,
                    clinic_id=row.clinic_id,
                    license_number=row.license_number,
                    years_of_experience=row.years_of_experience,
                    is_active=row.is_active,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]

            return PaginatedResponse(items=items, total=total)
