from pyodbc import Error

from src.config.database import get_pyodbc_connection
from src.schemas.user_schema import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from src.core.security import hash_password
from src.core.exceptions import (
    Errors,
    ExceptionFactory,
)
from typing import List


class UserService:

    @staticmethod
    def create_user(user_data: UserCreateSchema):

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check username
                cursor.execute(
                    """
                    SELECT user_id
                    FROM [User]
                    WHERE username = ?
                    """,
                    (user_data.username,),
                )

                if cursor.fetchone():
                    raise Errors.user_exists()

                # Check email
                cursor.execute(
                    """
                    SELECT user_id
                    FROM [User]
                    WHERE email = ?
                    """,
                    (user_data.email,),
                )

                if cursor.fetchone():
                    raise Errors.email_exists()

                # Hash password
                password_hash = hash_password(user_data.password)

                # Insert user
                cursor.execute(
                    """
                    INSERT INTO [User]
                    (
                        username,
                        password_hash,
                        first_name,
                        last_name,
                        email,
                        phone
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        user_data.username,
                        password_hash,
                        user_data.first_name,
                        user_data.last_name,
                        user_data.email,
                        user_data.phone,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error("Failed to create user")

    @staticmethod
    def get_user_by_id(user_id: int) -> UserResponseSchema:

        try:

            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT
                        user_id,
                        username,
                        first_name,
                        last_name,
                        email,
                        phone,
                        is_active
                    FROM [User]
                    WHERE user_id = ?
                    """,
                    (user_id,),
                )

                row = cursor.fetchone()

                if not row:
                    raise Errors.user_not_found()

                return UserResponseSchema(
                    user_id=row.user_id,
                    username=row.username,
                    first_name=row.first_name,
                    last_name=row.last_name,
                    email=row.email,
                    phone=row.phone,
                    is_active=row.is_active,
                )

        except Error:
            raise ExceptionFactory.server_error("Failed to retrieve user")

    @staticmethod
    def get_all_users() -> List[UserResponseSchema]:

        all_users = []

        try:

            with get_pyodbc_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT
                        user_id,
                        username,
                        first_name,
                        last_name,
                        email,
                        phone,
                        is_active
                    FROM [User]
                    """)

                rows = cursor.fetchall()

                # return
                for row in rows:
                    all_users.append(
                        UserResponseSchema(
                            user_id=row.user_id,
                            username=row.username,
                            first_name=row.first_name,
                            last_name=row.last_name,
                            email=row.email,
                            phone=row.phone,
                            is_active=row.is_active,
                        )
                    )

                return all_users

        except Error:
            raise ExceptionFactory.server_error("Failed to retrieve user")

    @staticmethod
    def update_user(user_id: int, user_data: UserUpdateSchema):

        try:

            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check user exists
                cursor.execute(
                    """
                    SELECT user_id
                    FROM [User]
                    WHERE user_id = ?
                    """,
                    (user_id,),
                )

                if not cursor.fetchone():
                    raise Errors.user_not_found()

                # Check email
                cursor.execute(
                    """
                    SELECT user_id
                    FROM [User]
                    WHERE email = ?
                    AND user_id <> ?
                    """,
                    (
                        user_data.email,
                        user_id,
                    ),
                )

                if cursor.fetchone():
                    raise Errors.email_exists()

                # Update
                cursor.execute(
                    """
                    UPDATE [User]
                    SET
                        first_name = ?,
                        last_name = ?,
                        email = ?,
                        phone = ?,
                        is_active = ?
                    WHERE user_id = ?
                    """,
                    (
                        user_data.first_name,
                        user_data.last_name,
                        user_data.email,
                        user_data.phone,
                        user_data.is_active,
                        user_id,
                    ),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error("Failed to update user")

    @staticmethod
    def delete_user(user_id: int):

        try:
            with get_pyodbc_connection() as conn:

                cursor = conn.cursor()

                # Check user exists
                cursor.execute(
                    """
                    SELECT user_id
                    FROM [User]
                    WHERE user_id = ?
                    """,
                    (user_id,),
                )

                if not cursor.fetchone():
                    raise Errors.user_not_found()

                cursor.execute(
                    """
                    DELETE FROM [User]
                    WHERE user_id = ?
                    """,
                    (user_id,),
                )

                conn.commit()

        except Error:
            raise ExceptionFactory.server_error("Failed to delete user")


