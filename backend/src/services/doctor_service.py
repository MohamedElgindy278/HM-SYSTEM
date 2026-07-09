from typing import List

from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from src.schemas.doctor_schema import (
    DoctorCreateSchema,
    DoctorUpdateSchema,
    DoctorResponseSchema,
)


class DoctorService:
    @staticmethod
    def create_doctor(
        doctor_data: DoctorCreateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                # Check user exists
                cursor.execute(
                    """

                    SELECT user_id
                    FROM [User]
                    WHERE user_id=?
                    """,
                    (doctor_data.user_id,),
                )

                if not cursor.fetchone():
                    raise Errors.user_not_found()

                # Check specialty exists
                cursor.execute(
                    """

                    SELECT specialty_id
                    FROM [Specialty]
                    WHERE specialty_id=?
                    """,
                    (doctor_data.specialty_id,),
                )

                if not cursor.fetchone():
                    raise Errors.specialty_not_found()

                # Check user is not already assigned as a doctor
                cursor.execute(
                    """

                    SELECT doctor_id
                    FROM [Doctor]
                    WHERE user_id=?
                    """,
                    (doctor_data.user_id,),
                )

                if cursor.fetchone():
                    raise Errors.doctor_exists()

                # Check license number already exists
                cursor.execute(
                    """

                    SELECT doctor_id
                    FROM [Doctor]
                    WHERE license_number=?
                    """,
                    (doctor_data.license_number,),
                )

                if cursor.fetchone():
                    raise Errors.doctor_license_exists()

                # Insert doctor
                cursor.execute(
                    """

                    INSERT INTO [Doctor]
                    (
                        user_id,
                        specialty_id,
                        license_number,
                        years_of_experience
                    )
                    VALUES
                    (
                        ?, ?, ?, ?
                    )
                    """,
                    (
                        doctor_data.user_id,
                        doctor_data.specialty_id,
                        doctor_data.license_number,
                        doctor_data.years_of_experience,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create doctor",
            )

    @staticmethod
    def update_doctor(
        doctor_id: int,
        doctor_data: DoctorUpdateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                # Check doctor exists
                cursor.execute(
                    """

                    SELECT doctor_id
                    FROM [Doctor]
                    WHERE doctor_id=?
                    """,
                    (doctor_id,),
                )

                if not cursor.fetchone():
                    raise Errors.doctor_not_found()

                # Check user exists
                cursor.execute(
                    """

                    SELECT user_id
                    FROM [User]
                    WHERE user_id=?
                    """,
                    (doctor_data.user_id,),
                )

                if not cursor.fetchone():
                    raise Errors.user_not_found()

                # Check specialty exists
                cursor.execute(
                    """

                    SELECT specialty_id
                    FROM [Specialty]
                    WHERE specialty_id=?
                    """,
                    (doctor_data.specialty_id,),
                )

                if not cursor.fetchone():
                    raise Errors.specialty_not_found()

                # Check user is not already assigned as a doctor
                cursor.execute(
                    """

                    SELECT doctor_id
                    FROM [Doctor]
                    WHERE user_id = ?
                    AND doctor_id <> ?
                    """,
                    (
                        doctor_data.user_id,
                        doctor_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.doctor_exists()

                # Check license number already exists
                cursor.execute(
                    """

                    SELECT doctor_id
                    FROM [Doctor]
                    WHERE license_number = ?
                    AND doctor_id <> ?
                    """,
                    (
                        doctor_data.license_number,
                        doctor_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.doctor_license_exists()

                # Update doctor
                cursor.execute(
                    """

                    UPDATE [Doctor]
                    SET
                        user_id=?,
                        specialty_id=?,
                        license_number=?,
                        years_of_experience=?
                    WHERE doctor_id=?
                    """,
                    (
                        doctor_data.user_id,
                        doctor_data.specialty_id,
                        doctor_data.license_number,
                        doctor_data.years_of_experience,
                        doctor_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update doctor",
            )

    @staticmethod
    def get_doctor_by_id(
        doctor_id: int,
    ) -> DoctorResponseSchema:

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT 
                        doctor_id,
                        user_id,
                        specialty_id,
                        license_number,
                        years_of_experience
                    FROM [Doctor]
                    WHERE doctor_id=?
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
                    license_number=row.license_number,
                    years_of_experience=row.years_of_experience,
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve doctor",
            )

    @staticmethod
    def get_all_doctors() -> List[DoctorResponseSchema]:

        doctors = []

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""

                    SELECT 
                        doctor_id,
                        user_id,
                        specialty_id,
                        license_number,
                        years_of_experience
                    FROM [Doctor]
                    """)

                rows = cursor.fetchall()

                for row in rows:
                    doctors.append(
                        DoctorResponseSchema(
                            doctor_id=row.doctor_id,
                            user_id=row.user_id,
                            specialty_id=row.specialty_id,
                            license_number=row.license_number,
                            years_of_experience=row.years_of_experience,
                        )
                    )

                return doctors

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve doctor",
            )
