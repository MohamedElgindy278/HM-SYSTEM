from typing import List

from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from src.schemas.specialty_schema import (
    SpecialtyCreateSchema,
    SpecialtyUpdateSchema,
    SpecialtyResponseSchema,
)


class SpecialtyService:

    @staticmethod
    def create_specialty(
        specialty_data: SpecialtyCreateSchema,
    ):

        try:

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
                    (
                        specialty_data.department_id,
                        specialty_data.name,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.specialty_exists()

                # Insert specialty
                cursor.execute(
                    """
                    INSERT INTO [Specialty]
                    (
                        department_id,
                        name,
                        description,
                        appointment_duration
                    )
                    VALUES
                    (
                        ?, ?, ?, ?
                    )
                    """,
                    (
                        specialty_data.department_id,
                        specialty_data.name,
                        specialty_data.description,
                        specialty_data.appointment_duration,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create specialty",
            )

    @staticmethod
    def update_specialty(
        specialty_id: int,
        specialty_data: SpecialtyUpdateSchema,
    ):

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check specialty exists
                cursor.execute(
                    """
                    SELECT specialty_id
                    FROM [Specialty]
                    WHERE specialty_id = ?
                    """,
                    (specialty_id,),
                )

                if not cursor.fetchone():
                    raise Errors.specialty_not_found()

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
                    AND specialty_id <> ?
                    """,
                    (
                        specialty_data.department_id,
                        specialty_data.name,
                        specialty_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.specialty_exists()

                # Update specialty
                cursor.execute(
                    """
                    UPDATE [Specialty]
                    SET
                        department_id = ?,
                        name = ?,
                        description = ?,
                        appointment_duration=?
                    WHERE specialty_id = ?
                    """,
                    (
                        specialty_data.department_id,
                        specialty_data.name,
                        specialty_data.description,
                        specialty_data.appointment_duration,
                        specialty_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update specialty",
            )

    @staticmethod
    def get_specialty_by_id(
        specialty_id: int,
    ) -> SpecialtyResponseSchema:

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT 
                        specialty_id,
                        department_id,
                        name,
                        description,
                        appointment_duration
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
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve specialty",
            )

    @staticmethod
    def get_all_specialties() -> List[SpecialtyResponseSchema]:

        specialties = []

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                cursor.execute("""
                    SELECT 
                        specialty_id,
                        department_id,
                        name,
                        description,
                        appointment_duration
                    FROM [Specialty]
                    """)

                rows = cursor.fetchall()

                for row in rows:
                    specialties.append(
                        SpecialtyResponseSchema(
                            specialty_id=row.specialty_id,
                            department_id=row.department_id,
                            name=row.name,
                            description=row.description,
                            appointment_duration=row.appointment_duration,
                        )
                    )

                return specialties

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve specialties",
            )
