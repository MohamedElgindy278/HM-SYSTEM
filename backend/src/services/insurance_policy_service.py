from typing import Optional

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.common_schema import PaginatedResponse
from src.schemas.insurance_policy_schema import (
    InsurancePolicyCreateSchema,
    InsurancePolicyResponseSchema,
    InsurancePolicyUpdateSchema,
)
from src.core.query_utils import build_where_clause, paginate


class InsurancePolicyService:

    @staticmethod
    @handle_db_errors("Failed to create insurance policy")
    def create_insurance_policy(insurance_data: InsurancePolicyCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check patient exists
            cursor.execute(
                "SELECT patient_id FROM [Patient] WHERE patient_id = ? AND is_deleted = 0",
                (insurance_data.patient_id,),
            )
            if not cursor.fetchone():
                raise Errors.patient_not_found()

            # Check provider exists
            cursor.execute(
                "SELECT provider_id FROM [InsuranceProvider] WHERE provider_id = ?",
                (insurance_data.provider_id,),
            )
            if not cursor.fetchone():
                raise Errors.insurance_provider_not_found()

            # Check policy number exists
            cursor.execute(
                "SELECT policy_id FROM [InsurancePolicy] WHERE policy_number = ?",
                (insurance_data.policy_number,),
            )
            if cursor.fetchone():
                raise Errors.insurance_policy_exists()

            # Check patient doesn't already have an active policy
            if insurance_data.is_active:
                cursor.execute(
                    "SELECT policy_id FROM [InsurancePolicy] WHERE patient_id = ? AND is_active = 1",
                    (insurance_data.patient_id,),
                )
                if cursor.fetchone():
                    raise Errors.patient_has_active_policy()

            cursor.execute(
                """
                INSERT INTO [InsurancePolicy]
                (
                    patient_id, provider_id, policy_number,
                    coverage_percentage, start_date, end_date, is_active
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
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

    @staticmethod
    @handle_db_errors("Failed to update insurance policy")
    def update_insurance_policy(
        policy_id: int,
        insurance_data: InsurancePolicyUpdateSchema,
    ) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Fetch current row
            cursor.execute(
                """
                SELECT
                    patient_id, provider_id, policy_number,
                    coverage_percentage, start_date, end_date, is_active
                FROM [InsurancePolicy]
                WHERE policy_id = ?
                """,
                (policy_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.insurance_policy_not_found()

            # Merge sent fields with current values
            fields = insurance_data.model_dump(exclude_unset=True)

            provider_id = fields.get("provider_id", row.provider_id)
            policy_number = fields.get("policy_number", row.policy_number)
            coverage_percentage = fields.get(
                "coverage_percentage", row.coverage_percentage
            )
            start_date = fields.get("start_date", row.start_date)
            end_date = fields.get("end_date", row.end_date)
            is_active = fields.get("is_active", row.is_active)

            if end_date and start_date and end_date < start_date:
                raise Errors.validation_error("end_date must be on or after start_date")

            # Check provider exists only if it changed
            if provider_id != row.provider_id:
                cursor.execute(
                    "SELECT provider_id FROM [InsuranceProvider] WHERE provider_id = ?",
                    (provider_id,),
                )
                if not cursor.fetchone():
                    raise Errors.insurance_provider_not_found()

            # Check policy number uniqueness only if it changed
            if policy_number != row.policy_number:
                cursor.execute(
                    "SELECT policy_id FROM [InsurancePolicy] WHERE policy_number = ? AND policy_id <> ?",
                    (policy_number, policy_id),
                )
                if cursor.fetchone():
                    raise Errors.insurance_policy_exists()

            # Check the one-active-policy-per-patient rule if this
            # update is turning the policy active
            if is_active and not row.is_active:
                cursor.execute(
                    """
                    SELECT policy_id FROM [InsurancePolicy]
                    WHERE patient_id = ? AND is_active = 1 AND policy_id <> ?
                    """,
                    (row.patient_id, policy_id),
                )
                if cursor.fetchone():
                    raise Errors.patient_has_active_policy()

            cursor.execute(
                """
                UPDATE [InsurancePolicy]
                SET
                    provider_id = ?, policy_number = ?, coverage_percentage = ?,
                    start_date = ?, end_date = ?, is_active = ?, updated_at = GETDATE()
                WHERE policy_id = ?
                """,
                (
                    provider_id,
                    policy_number,
                    coverage_percentage,
                    start_date,
                    end_date,
                    is_active,
                    policy_id,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve insurance policy")
    def get_insurance_policy_by_id(policy_id: int) -> InsurancePolicyResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    policy_id, patient_id, provider_id, policy_number,
                    coverage_percentage, start_date, end_date, is_active,
                    created_at, updated_at
                FROM [InsurancePolicy]
                WHERE policy_id = ?
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
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve insurance policies")
    def get_all_insurance_policies(
        start_num: int = 1,
        page_size: int = 20,
        patient_id: Optional[int] = None,
    ) -> PaginatedResponse[InsurancePolicyResponseSchema]:

        where_clause, params = build_where_clause(
            [
                ("patient_id = ?", patient_id),
            ]
        )

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT COUNT(*) AS total FROM [InsurancePolicy] {where_clause}",
                params,
            )
            total = cursor.fetchone().total

            cursor.execute(
                f"""
                SELECT
                    policy_id, patient_id, provider_id, policy_number,
                    coverage_percentage, start_date, end_date, is_active,
                    created_at, updated_at
                FROM [InsurancePolicy]
                {where_clause}
                ORDER BY policy_id
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                params + [offset, limit],
            )
            rows = cursor.fetchall()

            items = [
                InsurancePolicyResponseSchema(
                    policy_id=row.policy_id,
                    patient_id=row.patient_id,
                    provider_id=row.provider_id,
                    policy_number=row.policy_number,
                    coverage_percentage=row.coverage_percentage,
                    start_date=row.start_date,
                    end_date=row.end_date,
                    is_active=row.is_active,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]

            return PaginatedResponse(items=items, total=total)
