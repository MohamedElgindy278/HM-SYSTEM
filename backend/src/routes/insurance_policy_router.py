from fastapi import APIRouter

from src.core.responses import Responses
from src.schemas.insurance_policy_schema import (
    InsurancePolicyCreateSchema,
    InsurancePolicyUpdateSchema,
)
from src.services.insurance_policy_service import (
    InsurancePolicyService,
)

router = APIRouter(
    prefix="/insurance-policies",
    tags=["Insurance Policies"],
)

# ==========================
# Create
# ==========================


@router.post("/")
def create_insurance_policy(
    insurance_data: InsurancePolicyCreateSchema,
):

    InsurancePolicyService.create_insurance_policy(
        insurance_data,
    )

    return Responses.ok(
        message="Insurance policy created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("/")
def get_all_insurance_policies():

    return Responses.ok(
        data=InsurancePolicyService.get_all_insurance_policies(),
    )


@router.get("/{policy_id}")
def get_insurance_policy_by_id(
    policy_id: int,
):

    return Responses.ok(
        data=InsurancePolicyService.get_insurance_policy_by_id(
            policy_id,
        ),
    )


# ==========================
# Update
# ==========================


@router.put("/{policy_id}")
def update_insurance_policy(
    policy_id: int,
    insurance_data: InsurancePolicyUpdateSchema,
):

    InsurancePolicyService.update_insurance_policy(
        policy_id,
        insurance_data,
    )

    return Responses.ok(
        message="Insurance policy updated successfully",
    )
