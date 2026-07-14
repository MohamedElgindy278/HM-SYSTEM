from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.deps import require_permission
from src.core.responses import Responses
from src.schemas.department_schema import (
    DepartmentCreateSchema,
    DepartmentUpdateSchema,
)
from src.services.department_service import DepartmentService

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)

# ==========================
# Create
# ==========================


@router.post(
    "",
    status_code=201,
    dependencies=[Depends(require_permission("department:create"))],
)
def create_department(department_data: DepartmentCreateSchema):

    DepartmentService.create_department(department_data)

    return Responses.created(message="Department created successfully")


# ==========================
# Read
# ==========================


@router.get(
    "",
    dependencies=[Depends(require_permission("department:read"))],
)
def get_all_departments(
    branch_id: Optional[int] = Query(default=None),
):

    return Responses.ok(
        data=DepartmentService.get_all_departments(branch_id),
    )


@router.get(
    "/{department_id}",
    dependencies=[Depends(require_permission("department:read"))],
)
def get_department_by_id(department_id: int):

    return Responses.ok(
        data=DepartmentService.get_department_by_id(department_id),
    )


# ==========================
# Update
# ==========================


@router.put(
    "/{department_id}",
    dependencies=[Depends(require_permission("department:update"))],
)
def update_department(department_id: int, department_data: DepartmentUpdateSchema):

    DepartmentService.update_department(department_id, department_data)

    return Responses.ok(message="Department updated successfully")
