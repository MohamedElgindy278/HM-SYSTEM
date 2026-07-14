from typing import List, Optional

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.specialty_schema import (
    SpecialtyCreateSchema,
    SpecialtyResponseSchema,
    SpecialtyUpdateSchema,
)


class SpecialtyService:

    @staticmethod
    @handle_db_errors("Failed to create specialty")
    def create_specialty(specialty_data: SpecialtyCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check department exists
            cursor.execute(
                """
                
                SELECT department_id
                FROM [Department] 
                WHERE department_id = ?
                """,
                (specialty_data.department_id,),
            )
            if not cursor.fetchone():
                raise Errors.department_not_found()

            # Check specialty already exists in the department
            cursor.execute(
                """
                SELECT specialty_id
                FROM [Specialty]
                WHERE department_id = ?
                AND name = ?
                """,
                (specialty_data.department_id, specialty_data.name),
            )
            if cursor.fetchone():
                raise Errors.specialty_exists()

            cursor.execute(
                """
                INSERT INTO [Specialty]
                (
                    department_id,
                    name,
                    description,
                    appointment_duration
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    specialty_data.department_id,
                    specialty_data.name,
                    specialty_data.description,
                    specialty_data.appointment_duration,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to update specialty")
    def update_specialty(
        specialty_id: int,
        specialty_data: SpecialtyUpdateSchema,
    ) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT department_id, name, description, appointment_duration
                FROM [Specialty]
                WHERE specialty_id = ?
                """,
                (specialty_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.specialty_not_found()

            fields = specialty_data.model_dump(exclude_unset=True)

            department_id = fields.get("department_id", row.department_id)
            name = fields.get("name", row.name)
            description = fields.get("description", row.description)
            appointment_duration = fields.get(
                "appointment_duration", row.appointment_duration
            )

            # Check department exists
            cursor.execute(
                """
                SELECT department_id
                FROM [Department]
                WHERE department_id = ?
                """,
                (department_id,),
            )
            if not cursor.fetchone():
                raise Errors.department_not_found()

            # Check specialty already exists
            cursor.execute(
                """
                SELECT specialty_id
                FROM [Specialty]
                WHERE department_id = ?
                AND name = ?
                AND specialty_id <> ?
                """,
                (department_id, name, specialty_id),
            )
            if cursor.fetchone():
                raise Errors.specialty_exists()

            cursor.execute(
                """
                UPDATE [Specialty]
                SET
                    department_id = ?,
                    name = ?,
                    description = ?,
                    appointment_duration = ?,
                    updated_at = GETDATE()
                WHERE specialty_id = ?
                """,
                (department_id, name, description, appointment_duration, specialty_id),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve specialty")
    def get_specialty_by_id(specialty_id: int) -> SpecialtyResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    specialty_id, department_id, name,
                    description, appointment_duration,
                    created_at, updated_at
                FROM [Specialty]
                WHERE specialty_id = ?
                """,
                (specialty_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.specialty_not_found()

            return SpecialtyResponseSchema(
                specialty_id=row.specialty_id,
                department_id=row.department_id,
                name=row.name,
                description=row.description,
                appointment_duration=row.appointment_duration,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve specialties")
    def get_all_specialties(
        department_id: Optional[int] = None,
    ) -> List[SpecialtyResponseSchema]:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            if department_id is not None:
                cursor.execute(
                    """
                    SELECT
                        specialty_id, department_id, name,
                        description, appointment_duration,
                        created_at, updated_at
                    FROM [Specialty]
                    WHERE department_id = ?
                    ORDER BY name
                    """,
                    (department_id,),
                )
            else:
                cursor.execute("""
                    SELECT
                        specialty_id, department_id, name,
                        description, appointment_duration,
                        created_at, updated_at
                    FROM [Specialty]
                    ORDER BY name
                    """)

            rows = cursor.fetchall()

            return [
                SpecialtyResponseSchema(
                    specialty_id=row.specialty_id,
                    department_id=row.department_id,
                    name=row.name,
                    description=row.description,
                    appointment_duration=row.appointment_duration,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]
