from typing import Optional

from pyodbc import IntegrityError

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.core.query_utils import build_where_clause, paginate
from src.schemas.clinic_schema import (
    ClinicCreateSchema,
    ClinicResponseSchema,
    ClinicUpdateSchema,
)
from src.schemas.common_schema import PaginatedResponse


class ClinicService:

    @staticmethod
    @handle_db_errors("Failed to create clinic")
    def create_clinic(clinic_data: ClinicCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check department exists
            cursor.execute(
                "SELECT department_id FROM [Department] WHERE department_id = ?",
                (clinic_data.department_id,),
            )
            if not cursor.fetchone():
                raise Errors.department_not_found()

            try:
                cursor.execute(
                    """
                    INSERT INTO [Clinic]
                    (department_id, name, room_number, floor_number, is_active)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        clinic_data.department_id,
                        clinic_data.name,
                        clinic_data.room_number,
                        clinic_data.floor_number,
                        clinic_data.is_active,
                    ),
                )
                conn.commit()

            except IntegrityError as e:
                if "UQ_Clinic_DepartmentName" in str(e):
                    raise Errors.clinic_exists()
                raise

    @staticmethod
    @handle_db_errors("Failed to update clinic")
    def update_clinic(clinic_id: int, clinic_data: ClinicUpdateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT department_id, name, room_number, floor_number, is_active
                FROM [Clinic]
                WHERE clinic_id = ?
                """,
                (clinic_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.clinic_not_found()

            fields = clinic_data.model_dump(exclude_unset=True)

            department_id = fields.get("department_id", row.department_id)
            name = fields.get("name", row.name)
            room_number = fields.get("room_number", row.room_number)
            floor_number = fields.get("floor_number", row.floor_number)
            is_active = fields.get("is_active", row.is_active)

            if department_id != row.department_id:
                cursor.execute(
                    "SELECT department_id FROM [Department] WHERE department_id = ?",
                    (department_id,),
                )
                if not cursor.fetchone():
                    raise Errors.department_not_found()

            try:
                cursor.execute(
                    """
                    UPDATE [Clinic]
                    SET department_id = ?, name = ?, room_number = ?, floor_number = ?, is_active = ?
                    WHERE clinic_id = ?
                    """,
                    (
                        department_id,
                        name,
                        room_number,
                        floor_number,
                        is_active,
                        clinic_id,
                    ),
                )
                conn.commit()

            except IntegrityError as e:
                if "UQ_Clinic_DepartmentName" in str(e):
                    raise Errors.clinic_exists()
                raise

    @staticmethod
    @handle_db_errors("Failed to retrieve clinic")
    def get_clinic_by_id(clinic_id: int) -> ClinicResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT clinic_id, department_id, name, room_number, floor_number,
                       is_active, created_at
                FROM [Clinic]
                WHERE clinic_id = ?
                """,
                (clinic_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.clinic_not_found()

            return ClinicResponseSchema(
                clinic_id=row.clinic_id,
                department_id=row.department_id,
                name=row.name,
                room_number=row.room_number,
                floor_number=row.floor_number,
                is_active=row.is_active,
                created_at=row.created_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve clinics")
    def get_all_clinics(
        start_num: int = 1,
        page_size: int = 20,
        department_id: Optional[int] = None,
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[ClinicResponseSchema]:

        where_clause, params = build_where_clause(
            [
                ("department_id = ?", department_id),
                ("is_active = ?", is_active),
            ]
        )

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT COUNT(*) AS total FROM [Clinic] {where_clause}", params
            )
            total = cursor.fetchone().total

            cursor.execute(
                f"""
                SELECT clinic_id, department_id, name, room_number, floor_number,
                       is_active, created_at
                FROM [Clinic]
                {where_clause}
                ORDER BY name
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                params + [offset, limit],
            )
            rows = cursor.fetchall()

            items = [
                ClinicResponseSchema(
                    clinic_id=row.clinic_id,
                    department_id=row.department_id,
                    name=row.name,
                    room_number=row.room_number,
                    floor_number=row.floor_number,
                    is_active=row.is_active,
                    created_at=row.created_at,
                )
                for row in rows
            ]

            return PaginatedResponse(items=items, total=total)
