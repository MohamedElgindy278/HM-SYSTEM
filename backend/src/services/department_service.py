from typing import List

from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.core.exceptions import Errors, ExceptionFactory
from src.schemas.department_schema import (
    DepartmentCreateSchema,
    DepartmentUpdateSchema,
    DepartmentResponseSchema,
)


class DepartmentService:
    @staticmethod
    def create_department(
        department_data: DepartmentCreateSchema,
    ):

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()


                # Check branch exists
                cursor.execute(
                    """
                    SELECT branch_id
                    FROM [Branch]
                    WHERE branch_id = ?
                    """,
                    (department_data.branch_id,),
                )

                if not cursor.fetchone():
                    raise Errors.branch_not_found()

                # Check department name already exists in the branch
                cursor.execute(
                    """
                    SELECT department_id
                    FROM [Department]
                    WHERE branch_id = ?
                    AND name = ?
                    """,
                    (
                        department_data.branch_id,
                        department_data.name,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.department_exists()

                # Insert department
                cursor.execute(
                    """
                    INSERT INTO [Department]
                    (
                        branch_id,
                        name,
                        description
                    )
                    VALUES
                    (
                        ?, ?, ?
                    )
                    """,
                    (
                        department_data.branch_id,
                        department_data.name,
                        department_data.description,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to create department",
            )

    @staticmethod
    def update_department(
        department_id: int,
        department_data: DepartmentUpdateSchema,
    ):

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()


                # Check department exists
                cursor.execute(
                    """
                    SELECT department_id
                    FROM [Department]
                    WHERE department_id = ?
                    """,
                    (department_id,),
                )

                if not cursor.fetchone():
                    raise Errors.department_not_found()

                # Check branch exists
                cursor.execute(
                    """
                    SELECT branch_id
                    FROM [Branch]
                    WHERE branch_id = ?
                    """,
                    (department_data.branch_id,),
                )

                if not cursor.fetchone():
                    raise Errors.branch_not_found()

                # Check department name already exists in the branch
                cursor.execute(
                    """
                    SELECT department_id
                    FROM [Department]
                    WHERE branch_id = ?
                    AND name = ?
                    AND department_id <> ?
                    """,
                    (
                        department_data.branch_id,
                        department_data.name,
                        department_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.department_exists()

                # Update department
                cursor.execute(
                    """
                    UPDATE [Department]
                    SET
                        branch_id = ?,
                        name = ?,
                        description = ?
                    WHERE department_id = ?
                    """,
                    (
                        department_data.branch_id,
                        department_data.name,
                        department_data.description,
                        department_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to update department",
            )

    @staticmethod
    def get_department_by_id(
        department_id: int,
    ) -> DepartmentResponseSchema:

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """

                    SELECT 
                        department_id,
                        branch_id,
                        name,
                        description
                    FROM [Department]
                    WHERE department_id=?
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
                )

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve department",
            )

    @staticmethod
    def get_all_departments() -> List[DepartmentResponseSchema]:

        departments = []

        try:
            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""

                    SELECT 
                        department_id,
                        branch_id,
                        name,
                        description
                    FROM [Department]
                    """)

                rows = cursor.fetchall()

                for row in rows:
                    departments.append(
                        DepartmentResponseSchema(
                            department_id=row.department_id,
                            branch_id=row.branch_id,
                            name=row.name,
                            description=row.description,
                        )
                    )

                return departments

        except Error:
            raise ExceptionFactory.server_error(
                "Failed to retrieve department",
            )
