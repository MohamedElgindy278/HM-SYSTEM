from typing import List, Optional

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.department_schema import (
    DepartmentCreateSchema,
    DepartmentResponseSchema,
    DepartmentUpdateSchema,
)


class DepartmentService:

    @staticmethod
    @handle_db_errors("Failed to create department")
    def create_department(department_data: DepartmentCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check branch exists
            cursor.execute(
                "SELECT branch_id FROM [Branch] WHERE branch_id = ?",
                (department_data.branch_id,),
            )
            if not cursor.fetchone():
                raise Errors.branch_not_found()

            # Check department name already exists in the branch
            cursor.execute(
                "SELECT department_id FROM [Department] WHERE branch_id = ? AND name = ?",
                (department_data.branch_id, department_data.name),
            )
            if cursor.fetchone():
                raise Errors.department_exists()

            cursor.execute(
                """
                INSERT INTO [Department]
                (branch_id, name, description)
                VALUES (?, ?, ?)
                """,
                (
                    department_data.branch_id,
                    department_data.name,
                    department_data.description,
                ),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to update department")
    def update_department(
        department_id: int,
        department_data: DepartmentUpdateSchema,
    ) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Fetch current row
            cursor.execute(
                "SELECT branch_id, name, description FROM [Department] WHERE department_id = ?",
                (department_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.department_not_found()

            # Merge sent fields with current values
            fields = department_data.model_dump(exclude_unset=True)

            branch_id = fields.get("branch_id", row.branch_id)
            name = fields.get("name", row.name)
            description = fields.get("description", row.description)

            # Check branch exists only if it changed
            if branch_id != row.branch_id:
                cursor.execute(
                    "SELECT branch_id FROM [Branch] WHERE branch_id = ?",
                    (branch_id,),
                )
                if not cursor.fetchone():
                    raise Errors.branch_not_found()

            # Check name uniqueness only if branch or name changed
            if branch_id != row.branch_id or name != row.name:
                cursor.execute(
                    """
                    SELECT department_id FROM [Department]
                    WHERE branch_id = ? AND name = ? AND department_id <> ?
                    """,
                    (branch_id, name, department_id),
                )
                if cursor.fetchone():
                    raise Errors.department_exists()

            cursor.execute(
                """
                UPDATE [Department]
                SET branch_id = ?, name = ?, description = ?, updated_at = GETDATE()
                WHERE department_id = ?
                """,
                (branch_id, name, description, department_id),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve department")
    def get_department_by_id(department_id: int) -> DepartmentResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT department_id, branch_id, name, description, created_at, updated_at
                FROM [Department]
                WHERE department_id = ?
                """,
                (department_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.department_not_found()

            return DepartmentResponseSchema(
                department_id=row.department_id,
                branch_id=row.branch_id,
                name=row.name,
                description=row.description,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve departments")
    def get_all_departments(
        branch_id: Optional[int] = None,
    ) -> List[DepartmentResponseSchema]:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            if branch_id is not None:
                cursor.execute(
                    """
                    SELECT department_id, branch_id, name, description, created_at, updated_at
                    FROM [Department]
                    WHERE branch_id = ?
                    ORDER BY name
                    """,
                    (branch_id,),
                )
            else:
                cursor.execute("""
                    SELECT department_id, branch_id, name, description, created_at, updated_at
                    FROM [Department]
                    ORDER BY name
                    """)

            rows = cursor.fetchall()

            return [
                DepartmentResponseSchema(
                    department_id=row.department_id,
                    branch_id=row.branch_id,
                    name=row.name,
                    description=row.description,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]
