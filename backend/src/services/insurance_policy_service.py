from typing import List

from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from src.schemas.insurance_policy_schema import (
    InsurancePolicyCreateSchema,
    InsurancePolicyUpdateSchema,
    InsurancePolicyResponseSchema,
)


class InsurancePolicyService:
    @staticmethod
    def create_insurance_policy(
        insurance_data: InsurancePolicyCreateSchema,
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
                    (insurance_data.patient_id,),
                )

                if not cursor.fetchone():
                    raise Errors.patient_not_found()

                # Check provider exists
                cursor.execute(
                    """
                    SELECT provider_id
                    FROM [InsuranceProvider]
                    WHERE provider_id = ?
                    """,
                    (insurance_data.provider_id,),
                )

                if not cursor.fetchone():
                    raise Errors.insurance_provider_not_found()

                # Check Policy Number exists
                cursor.execute(
                    """

                    SELECT policy_id
                    FROM [InsurancePolicy]
                    WHERE policy_number=?
                    """,
                    (insurance_data.policy_number,),
                )

                if cursor.fetchone():
                    raise Errors.insurance_policy_exists()

                # Check patient doesn't already have an active insurance policy
                cursor.execute(
                    """

                    SELECT policy_id
                    FROM [InsurancePolicy]
                    WHERE patient_id = ?
                    AND is_active = 1
                    """,
                    (insurance_data.patient_id,),
                )

                if cursor.fetchone():
                    raise Errors.patient_has_active_policy()

                cursor.execute(
                    """

                    INSERT INTO [InsurancePolicy]
                    (
                        patient_id,
                        provider_id,
                        policy_number,
                        coverage_percentage,
                        start_date,
                        end_date,
                        is_active
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        insurance_data.patient_id,
                        insurance_data.provider_id,
                        insurance_data.policy_number,
                        insurance_data.coverage_percentage,
                        insurance_data.start_date,
                        insurance_data.end_date,
                        insurance_data.is_active,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create insurance policy",
            )

    @staticmethod
    def update_insurance_policy(
        policy_id: int,
        insurance_data: InsurancePolicyUpdateSchema,
    ):

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                # Check policy exists
                cursor.execute(
                    """
                    SELECT policy_id
                    FROM [InsurancePolicy]
                    WHERE policy_id = ?
                    """,
                    (policy_id,),
                )

                if not cursor.fetchone():
                    raise Errors.insurance_policy_not_found()

                # Check provider exists
                cursor.execute(
                    """
                    SELECT provider_id
                    FROM [InsuranceProvider]
                    WHERE provider_id = ?
                    """,
                    (insurance_data.provider_id,),
                )

                if not cursor.fetchone():
                    raise Errors.insurance_provider_not_found()

                # Check policy number already exists
                cursor.execute(
                    """
                    SELECT policy_id
                    FROM [InsurancePolicy]
                    WHERE policy_number = ?
                    AND policy_id <> ?
                    """,
                    (
                        insurance_data.policy_number,
                        policy_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.insurance_policy_exists()

                # Update insurance policy
                cursor.execute(
                    """
                    UPDATE [InsurancePolicy]
                    SET
                        provider_id = ?,
                        policy_number = ?,
                        coverage_percentage = ?,
                        start_date = ?,
                        end_date = ?,
                        is_active = ?
                    WHERE policy_id = ?
                    """,
                    (
                        insurance_data.provider_id,
                        insurance_data.policy_number,
                        insurance_data.coverage_percentage,
                        insurance_data.start_date,
                        insurance_data.end_date,
                        insurance_data.is_active,
                        policy_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update insurance policy",
            )

    @staticmethod
    def get_insurance_policy_by_id(
        policy_id: int,
    ) -> InsurancePolicyResponseSchema:

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT 
                        policy_id,
                        patient_id,
                        provider_id,
                        policy_number,
                        coverage_percentage,
                        start_date,
                        end_date,
                        is_active
                    FROM [InsurancePolicy]
                    WHERE policy_id=?
                    """,
                    (policy_id,),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.insurance_policy_not_found()

                return InsurancePolicyResponseSchema(
                    policy_id=row.policy_id,
                    patient_id=row.patient_id,
                    provider_id=row.provider_id,
                    policy_number=row.policy_number,
                    coverage_percentage=row.coverage_percentage,
                    start_date=row.start_date,
                    end_date=row.end_date,
                    is_active=row.is_active,
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve insurance policies",
            )

    @staticmethod
    def get_all_insurance_policies() -> List[InsurancePolicyResponseSchema]:

        policies = []

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT 
                        policy_id,
                        patient_id,
                        provider_id,
                        policy_number,
                        coverage_percentage,
                        start_date,
                        end_date,
                        is_active
                    FROM [InsurancePolicy]
                    """,
                )

                rows = cursor.fetchall()

                for row in rows:
                    policies.append(
                        InsurancePolicyResponseSchema(
                            policy_id=row.policy_id,
                            patient_id=row.patient_id,
                            provider_id=row.provider_id,
                            policy_number=row.policy_number,
                            coverage_percentage=row.coverage_percentage,
                            start_date=row.start_date,
                            end_date=row.end_date,
                            is_active=row.is_active,
                        )
                    )

                return policies

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve insurance policy",
            )
