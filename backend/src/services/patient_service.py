from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.common_schema import PaginatedResponse
from src.schemas.patient_schema import (
    PatientCreateSchema,
    PatientResponseSchema,
    PatientUpdateSchema,
)
from src.core.query_utils import paginate


class PatientService:

    @staticmethod
    @handle_db_errors("Failed to create patient")
    def create_patient(patient_data: PatientCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check national ID only among active (non soft-deleted) patients
            if patient_data.national_id is not None:
                cursor.execute(
                    "SELECT patient_id FROM [Patient] WHERE national_id = ? AND is_deleted = 0",
                    (patient_data.national_id,),
                )
                if cursor.fetchone():
                    raise Errors.patient_national_id_exists()

            # mrn is deliberately not inserted here - DF_Patient_Mrn fills
            # a temporary '' value, then TR_CreateMRN overwrites it with
            # the real 'MRN-00001' style identifier right after insert.
            cursor.execute(
                """
                INSERT INTO [Patient]
                (
                    first_name, last_name, date_of_birth, gender,
                    national_id, phone, address,
                    emergency_contact_name, emergency_contact_phone
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
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

    @staticmethod
    @handle_db_errors("Failed to update patient")
    def update_patient(patient_id: int, patient_data: PatientUpdateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Fetch current row
            cursor.execute(
                """
                SELECT
                    first_name, last_name, date_of_birth, gender,
                    national_id, phone, address,
                    emergency_contact_name, emergency_contact_phone
                FROM [Patient]
                WHERE patient_id = ?
                AND is_deleted = 0
                """,
                (patient_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.patient_not_found()

            # Merge sent fields with current values
            fields = patient_data.model_dump(exclude_unset=True)

            first_name = fields.get("first_name", row.first_name)
            last_name = fields.get("last_name", row.last_name)
            date_of_birth = fields.get("date_of_birth", row.date_of_birth)
            gender = fields.get("gender", row.gender)
            national_id = fields.get("national_id", row.national_id)
            phone = fields.get("phone", row.phone)
            address = fields.get("address", row.address)
            emergency_contact_name = fields.get(
                "emergency_contact_name", row.emergency_contact_name
            )
            emergency_contact_phone = fields.get(
                "emergency_contact_phone", row.emergency_contact_phone
            )

            # Check national ID uniqueness only if it changed, and only
            # among active (non soft-deleted) patients
            if national_id is not None and national_id != row.national_id:
                cursor.execute(
                    """
                    SELECT patient_id
                    FROM [Patient]
                    WHERE national_id = ?
                    AND patient_id <> ?
                    AND is_deleted = 0
                    """,
                    (national_id, patient_id),
                )
                if cursor.fetchone():
                    raise Errors.patient_national_id_exists()

            cursor.execute(
                """
                UPDATE [Patient]
                SET
                    first_name = ?, last_name = ?, date_of_birth = ?, gender = ?,
                    national_id = ?, phone = ?, address = ?,
                    emergency_contact_name = ?, emergency_contact_phone = ?,
                    updated_at = GETDATE()
                WHERE patient_id = ?
                """,
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    national_id,
                    phone,
                    address,
                    emergency_contact_name,
                    emergency_contact_phone,
                    patient_id,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve patient")
    def get_patient_by_id(patient_id: int) -> PatientResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    patient_id, mrn, first_name, last_name, date_of_birth, gender,
                    national_id, phone, address,
                    emergency_contact_name, emergency_contact_phone,
                    created_at, updated_at
                FROM [Patient]
                WHERE patient_id = ?
                AND is_deleted = 0
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
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve patients")
    def get_all_patients(
        start_num: int = 1,
        page_size: int = 20,
    ) -> PaginatedResponse[PatientResponseSchema]:

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) AS total FROM [Patient] WHERE is_deleted = 0"
            )
            total = cursor.fetchone().total

            cursor.execute(
                """
                SELECT
                    patient_id, mrn, first_name, last_name, date_of_birth, gender,
                    national_id, phone, address,
                    emergency_contact_name, emergency_contact_phone,
                    created_at, updated_at
                FROM [Patient]
                WHERE is_deleted = 0
                ORDER BY patient_id
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                (offset, limit),
            )
            rows = cursor.fetchall()

            items = [
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
                    updated_at=row.updated_at,
                )
                for row in rows
            ]

            return PaginatedResponse(items=items, total=total)

    @staticmethod
    @handle_db_errors("Failed to delete patient")
    def delete_patient(patient_id: int) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT patient_id FROM [Patient] WHERE patient_id = ? AND is_deleted = 0",
                (patient_id,),
            )
            if not cursor.fetchone():
                raise Errors.patient_not_found()

            # Soft delete, medical records are never hard-deleted
            cursor.execute(
                "UPDATE [Patient] SET is_deleted = 1, deleted_at = GETDATE() WHERE patient_id = ?",
                (patient_id,),
            )
            conn.commit()
