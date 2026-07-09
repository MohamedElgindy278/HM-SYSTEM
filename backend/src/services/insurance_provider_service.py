from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.schemas.insurance_provider_schema import (
    InsuranceProviderCreateSchema,
    InsuranceProviderUpdateSchema,
    InsuranceProviderResponseSchema,
)

from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from typing import List


class InsuranceProviderService:
    @staticmethod
    def create_insurance_provider(
        insurance_data: InsuranceProviderCreateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                # Check provider name exists
                cursor.execute(
                    """
                    SELECT provider_id
                    FROM InsuranceProvider
                    WHERE name = ?
                    """,
                    (insurance_data.name,),
                )

                if cursor.fetchone():
                    raise Errors.insurance_provider_exists()

                # insert insurance_provider
                cursor.execute(
                    """
                    
                    INSERT INTO [InsuranceProvider]
                    (
                        name,
                        phone,
                        email
                    )
                    VALUES
                    (
                        ?, ?, ?
                    )
                    """,
                    (
                        insurance_data.name,
                        insurance_data.phone,
                        insurance_data.email,
                    ),
                )

                conn.commit()
        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create insurance provider",
            )

    @staticmethod
    def update_insurance_provider(
        provider_id: int,
        insurance_data: InsuranceProviderUpdateSchema,
    ):

        try:

            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                # Check provider exists
                cursor.execute(
                    """
                    SELECT provider_id
                    FROM [InsuranceProvider]
                    WHERE provider_id = ?
                    """,
                    (provider_id,),
                )

                if not cursor.fetchone():
                    raise Errors.insurance_provider_not_found()

                # Check provider name exists
                cursor.execute(
                    """
                    SELECT provider_id
                    FROM [InsuranceProvider]
                    WHERE name = ?
                    AND provider_id <> ?
                    """,
                    (
                        insurance_data.name,
                        provider_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.insurance_provider_exists()

                # Update insurance provider
                cursor.execute(
                    """
                    UPDATE [InsuranceProvider]
                    SET
                        name = ?,
                        phone = ?,
                        email = ?
                    WHERE provider_id = ?
                    """,
                    (
                        insurance_data.name,
                        insurance_data.phone,
                        insurance_data.email,
                        provider_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update insurance provider",
            )

    @staticmethod
    def get_insurance_provider_by_id(
        provider_id: int,
    ) -> InsuranceProviderResponseSchema:

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT 
                        provider_id,
                        name,
                        phone,
                        email
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
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve insurance provider",
            )

    @staticmethod
    def get_all_insurance_providers() -> List[InsuranceProviderResponseSchema]:

        providers = []

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    
                    SELECT 
                        provider_id,
                        name,
                        phone,
                        email
                    FROM [InsuranceProvider]
                    """)

                rows = cursor.fetchall()

                for row in rows:
                    providers.append(
                        InsuranceProviderResponseSchema(
                            provider_id=row.provider_id,
                            name=row.name,
                            phone=row.phone,
                            email=row.email,
                        )
                    )

                return providers

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve insurance provider",
            )
