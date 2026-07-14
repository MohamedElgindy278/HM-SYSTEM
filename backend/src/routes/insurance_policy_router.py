from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.insurance_policy_schema import (
    InsurancePolicyCreateSchema,
    InsurancePolicyUpdateSchema,
)
from src.services.insurance_policy_service import InsurancePolicyService

router = APIRouter(
    prefix="/insurance-policies",
    tags=["Insurance Policies"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("insurance_policy:create"))],
)
def create_insurance_policy(insurance_data: InsurancePolicyCreateSchema):

    InsurancePolicyService.create_insurance_policy(insurance_data)

    return Responses.created(message="Insurance policy created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("insurance_policy:read"))],
)
def get_all_insurance_policies(
    start_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    patient_id: Optional[int] = Query(default=None),
):

    return Responses.ok(
        data=InsurancePolicyService.get_all_insurance_policies(
            start_num, page_size, patient_id
        ),
    )


@router.get(
    "/{policy_id}",
    dependencies=[Depends(require_permission("insurance_policy:read"))],
)
def get_insurance_policy_by_id(policy_id: int):

    return Responses.ok(
        data=InsurancePolicyService.get_insurance_policy_by_id(policy_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{policy_id}",
    dependencies=[Depends(require_permission("insurance_policy:update"))],
)
def update_insurance_policy(
    policy_id: int, insurance_data: InsurancePolicyUpdateSchema
):

    InsurancePolicyService.update_insurance_policy(policy_id, insurance_data)

    return Responses.ok(message="Insurance policy updated successfully")
