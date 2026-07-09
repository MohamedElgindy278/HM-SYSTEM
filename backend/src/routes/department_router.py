from fastapi import APIRouter

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


@router.post("/")
def create_department(department_data: DepartmentCreateSchema):
    DepartmentService.create_department(
        department_data,
    )

    return Responses.ok(
        message="Department created successfully",
    )


# ==========================
# Read
# ==========================


@router.get("/")
def get_all_departments():

    return Responses.ok(
        data=DepartmentService.get_all_departments(),
    )


@router.get("/{department_id}")
def get_department_by_id(
    department_id: int,
):

    return Responses.ok(
        data=DepartmentService.get_department_by_id(
            department_id,
        ),
    )


# ==========================
# Update
# ==========================


@router.put("/{department_id}")
def update_department(
    department_id: int,
    department_data: DepartmentUpdateSchema,
):
    DepartmentService.update_department(
        department_id,
        department_data,
    )

    return Responses.ok(
        message="Department updated successfully",
    )
