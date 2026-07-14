from typing import List

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.insurance_provider_schema import (
    InsuranceProviderCreateSchema,
    InsuranceProviderResponseSchema,
    InsuranceProviderUpdateSchema,
)


class InsuranceProviderService:

    @staticmethod
    @handle_db_errors("Failed to create insurance provider")
    def create_insurance_provider(
        insurance_data: InsuranceProviderCreateSchema,
    ) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check provider name exists
            cursor.execute(
                "SELECT provider_id FROM [InsuranceProvider] WHERE name = ?",
                (insurance_data.name,),
            )
            if cursor.fetchone():
                raise Errors.insurance_provider_exists()

            cursor.execute(
                """
                INSERT INTO [InsuranceProvider]
                (name, phone, email)
                VALUES (?, ?, ?)
                """,
                (insurance_data.name, insurance_data.phone, insurance_data.email),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to update insurance provider")
    def update_insurance_provider(
        provider_id: int,
        insurance_data: InsuranceProviderUpdateSchema,
    ) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Fetch current row
            cursor.execute(
                "SELECT name, phone, email FROM [InsuranceProvider] WHERE provider_id = ?",
                (provider_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.insurance_provider_not_found()

            # Merge sent fields with current values
            fields = insurance_data.model_dump(exclude_unset=True)

            name = fields.get("name", row.name)
            phone = fields.get("phone", row.phone)
            email = fields.get("email", row.email)

            # Check name uniqueness only if it changed
            if name != row.name:
                cursor.execute(
                    "SELECT provider_id FROM [InsuranceProvider] WHERE name = ? AND provider_id <> ?",
                    (name, provider_id),
                )
                if cursor.fetchone():
                    raise Errors.insurance_provider_exists()

            cursor.execute(
                """
                UPDATE [InsuranceProvider]
                SET name = ?, phone = ?, email = ?, updated_at = GETDATE()
                WHERE provider_id = ?
                """,
                (name, phone, email, provider_id),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve insurance provider")
    def get_insurance_provider_by_id(
        provider_id: int,
    ) -> InsuranceProviderResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT provider_id, name, phone, email, created_at, updated_at
                FROM [InsuranceProvider]
                WHERE provider_id = ?
                """,
                (provider_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.insurance_provider_not_found()

            return InsuranceProviderResponseSchema(
                provider_id=row.provider_id,
                name=row.name,
                phone=row.phone,
                email=row.email,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve insurance providers")
    def get_all_insurance_providers() -> List[InsuranceProviderResponseSchema]:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT provider_id, name, phone, email, created_at, updated_at
                FROM [InsuranceProvider]
                ORDER BY name
                """)
            rows = cursor.fetchall()

            return [
                InsuranceProviderResponseSchema(
                    provider_id=row.provider_id,
                    name=row.name,
                    phone=row.phone,
                    email=row.email,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]
