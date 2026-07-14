from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.schemas.common_schema import PaginatedResponse
from src.schemas.user_schema import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from src.core.security import hash_password
from src.core.query_utils import paginate


class UserService:

    @staticmethod
    @handle_db_errors("Failed to create user")
    def create_user(user_data: UserCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            # Check username
            cursor.execute(
                """
                SELECT user_id
                FROM [User]
                WHERE username = ?
                AND is_deleted = 0
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
                AND is_deleted = 0
                """,
                (user_data.email,),
            )
            if cursor.fetchone():
                raise Errors.email_exists()

            password_hash = hash_password(user_data.password)

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
                VALUES (?, ?, ?, ?, ?, ?)
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

    @staticmethod
    @handle_db_errors("Failed to retrieve user")
    def get_user_by_id(user_id: int) -> UserResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    user_id, username, first_name, last_name,
                    email, phone, is_active, created_at, updated_at
                FROM [User]
                WHERE user_id = ?
                AND is_deleted = 0
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
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    @staticmethod
    @handle_db_errors("Failed to retrieve users")
    def get_all_users(
        start_num: int = 1,
        page_size: int = 20,
    ) -> PaginatedResponse[UserResponseSchema]:

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) AS total FROM [User] WHERE is_deleted = 0")
            total = cursor.fetchone().total

            cursor.execute(
                """
                SELECT
                    user_id, username, first_name, last_name,
                    email, phone, is_active, created_at, updated_at
                FROM [User]
                WHERE is_deleted = 0
                ORDER BY user_id
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                (offset, limit),
            )
            rows = cursor.fetchall()

            items = [
                UserResponseSchema(
                    user_id=row.user_id,
                    username=row.username,
                    first_name=row.first_name,
                    last_name=row.last_name,
                    email=row.email,
                    phone=row.phone,
                    is_active=row.is_active,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in rows
            ]

            return PaginatedResponse(items=items, total=total)

    @staticmethod
    @handle_db_errors("Failed to update user")
    def update_user(user_id: int, user_data: UserUpdateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT first_name, last_name, email, phone, is_active
                FROM [User]
                WHERE user_id = ?
                AND is_deleted = 0
                """,
                (user_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.user_not_found()

            fields = user_data.model_dump(exclude_unset=True)

            first_name = fields.get("first_name", row.first_name)
            last_name = fields.get("last_name", row.last_name)
            email = fields.get("email", row.email)
            phone = fields.get("phone", row.phone)
            is_active = fields.get("is_active", row.is_active)

            if email != row.email:
                cursor.execute(
                    """
                    SELECT user_id
                    FROM [User]
                    WHERE email = ?
                    AND user_id <> ?
                    AND is_deleted = 0
                    """,
                    (email, user_id),
                )
                if cursor.fetchone():
                    raise Errors.email_exists()

            cursor.execute(
                """
                UPDATE [User]
                SET
                    first_name = ?,
                    last_name = ?,
                    email = ?,
                    phone = ?,
                    is_active = ?,
                    updated_at = GETDATE()
                WHERE user_id = ?
                """,
                (first_name, last_name, email, phone, is_active, user_id),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to delete user")
    def delete_user(user_id: int) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT user_id
                FROM [User]
                WHERE user_id = ?
                AND is_deleted = 0
                """,
                (user_id,),
            )
            if not cursor.fetchone():
                raise Errors.user_not_found()

            cursor.execute(
                """
                UPDATE [User]
                SET
                    is_deleted = 1,
                    deleted_at = GETDATE(),
                    is_active = 0
                WHERE user_id = ?
                """,
                (user_id,),
            )
            conn.commit()
