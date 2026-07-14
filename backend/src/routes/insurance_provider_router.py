from fastapi import APIRouter, Depends

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.insurance_provider_schema import (
    InsuranceProviderCreateSchema,
    InsuranceProviderUpdateSchema,
)
from src.services.insurance_provider_service import InsuranceProviderService

router = APIRouter(
    prefix="/insurance-providers",
    tags=["Insurance Providers"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("insurance_provider:create"))],
)
def create_insurance_provider(insurance_data: InsuranceProviderCreateSchema):

    InsuranceProviderService.create_insurance_provider(insurance_data)

    return Responses.created(message="Provider created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("insurance_provider:read"))],
)
def get_all_insurance_providers():

    return Responses.ok(
        data=InsuranceProviderService.get_all_insurance_providers(),
    )


@router.get(
    "/{provider_id}",
    dependencies=[Depends(require_permission("insurance_provider:read"))],
)
def get_insurance_provider_by_id(provider_id: int):

    return Responses.ok(
        data=InsuranceProviderService.get_insurance_provider_by_id(provider_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{provider_id}",
    dependencies=[Depends(require_permission("insurance_provider:update"))],
)
def update_insurance_provider(
    provider_id: int,
    insurance_data: InsuranceProviderUpdateSchema,
):

    InsuranceProviderService.update_insurance_provider(provider_id, insurance_data)

    return Responses.ok(message="Provider updated successfully")
