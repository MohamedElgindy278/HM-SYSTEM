from typing import List

from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from src.schemas.patient_schema import (
    PatientCreateSchema,
    PatientUpdateSchema,
    PatientResponseSchema,
)


class PatientService:
    @staticmethod
    def create_patient(
        patient_data: PatientCreateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                # Check MRN already exists
                cursor.execute(
                    """

                    SELECT patient_id
                    FROM [Patient]
                    WHERE mrn=?
                    """,
                    (patient_data.mrn,),
                )

                if cursor.fetchone():
                    raise Errors.patient_mrn_exists()

                # Check National ID already exists
                if patient_data.national_id is not None:
                    cursor.execute(
                        """

                        SELECT patient_id
                        FROM [Patient]
                        WHERE national_id=?
                        """,
                        (patient_data.national_id,),
                    )

                    if cursor.fetchone():
                        raise Errors.patient_national_id_exists()

                # Insert patient
                cursor.execute(
                    """

                    INSERT INTO [Patient]
                    (
                        mrn,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        national_id,
                        phone,
                        address,
                        emergency_contact_name,
                        emergency_contact_phone
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        patient_data.mrn,
                        patient_data.first_name,
                        patient_data.last_name,
                        patient_data.date_of_birth,
                        patient_data.gender,
                        patient_data.national_id,
                        patient_data.phone,
                        patient_data.address,
                        patient_data.emergency_contact_name,
                        patient_data.emergency_contact_phone,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create patient",
            )

    @staticmethod
    def update_patient(
        patient_id: int,
        patient_data: PatientUpdateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                # Check Patient exists
                cursor.execute(
                    """

                    SELECT patient_id
                    FROM [Patient]
                    WHERE patient_id=?
                    """,
                    (patient_id,),
                )

                if not cursor.fetchone():
                    raise Errors.patient_not_found()

                # Check MRN already exists
                cursor.execute(
                    """

                    SELECT patient_id
                    FROM [Patient]
                    WHERE mrn=?
                    AND patient_id <> ?
                    """,
                    (
                        patient_data.mrn,
                        patient_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.patient_mrn_exists()

                # Check National ID already exists
                if patient_data.national_id is not None:
                    cursor.execute(
                        """

                        SELECT patient_id
                        FROM [Patient]
                        WHERE national_id=?
                        AND patient_id <> ?
                        """,
                        (
                            patient_data.national_id,
                            patient_id,
                        ),
                    )

                    if cursor.fetchone():
                        raise Errors.patient_national_id_exists()

                cursor.execute(
                    """

                    UPDATE [Patient]
                    SET
                        mrn = ?,
                        first_name = ?,
                        last_name = ?,
                        date_of_birth = ?,
                        gender = ?,
                        national_id = ?,
                        phone = ?,
                        address = ?,
                        emergency_contact_name = ?,
                        emergency_contact_phone = ?
                    WHERE patient_id = ?
                    """,
                    (
                        patient_data.mrn,
                        patient_data.first_name,
                        patient_data.last_name,
                        patient_data.date_of_birth,
                        patient_data.gender,
                        patient_data.national_id,
                        patient_data.phone,
                        patient_data.address,
                        patient_data.emergency_contact_name,
                        patient_data.emergency_contact_phone,
                        patient_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update patient",
            )

    @staticmethod
    def get_patient_by_id(
        patient_id: int,
    ) -> PatientResponseSchema:

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT
                        patient_id,
                        mrn,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        national_id,
                        phone,
                        address,
                        emergency_contact_name,
                        emergency_contact_phone,
                        created_at
                    FROM [Patient]
                    WHERE patient_id=?
                    """,
                    (patient_id,),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.patient_not_found()

                return PatientResponseSchema(
                    patient_id=row.patient_id,
                    mrn=row.mrn,
                    first_name=row.first_name,
                    last_name=row.last_name,
                    date_of_birth=row.date_of_birth,
                    gender=row.gender,
                    national_id=row.national_id,
                    phone=row.phone,
                    address=row.address,
                    emergency_contact_name=row.emergency_contact_name,
                    emergency_contact_phone=row.emergency_contact_phone,
                    created_at=row.created_at,
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve patient",
            )

    @staticmethod
    def get_all_patients() -> List[PatientResponseSchema]:

        patients = []

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT
                        patient_id,
                        mrn,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        national_id,
                        phone,
                        address,
                        emergency_contact_name,
                        emergency_contact_phone,
                        created_at
                    FROM [Patient]
                    """,
                )

                rows = cursor.fetchall()

                for row in rows:
                    patients.append(
                        PatientResponseSchema(
                            patient_id=row.patient_id,
                            mrn=row.mrn,
                            first_name=row.first_name,
                            last_name=row.last_name,
                            date_of_birth=row.date_of_birth,
                            gender=row.gender,
                            national_id=row.national_id,
                            phone=row.phone,
                            address=row.address,
                            emergency_contact_name=row.emergency_contact_name,
                            emergency_contact_phone=row.emergency_contact_phone,
                            created_at=row.created_at,
                        )
                    )

                return patients

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve patient",
            )
