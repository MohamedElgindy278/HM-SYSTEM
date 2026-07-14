from typing import List

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.core.security import decode_access_token
from src.schemas.auth_schema import CurrentUserSchema

bearer_scheme = HTTPBearer()


@handle_db_errors("Failed to authenticate user")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentUserSchema:

    user_id = decode_access_token(credentials.credentials)

    with get_pyodbc_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT user_id, username, is_active, is_deleted FROM [User] WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()

        if not row:
            raise Errors.user_not_found()

        if row.is_deleted:
            raise Errors.invalid_token()

        if not row.is_active:
            raise Errors.inactive_user()

        cursor.execute(
            """
            SELECT r.name
            FROM UserRole ur
            INNER JOIN Role r ON ur.role_id = r.role_id
            WHERE ur.user_id = ?
            """,
            (user_id,),
        )
        roles = [r.name for r in cursor.fetchall()]

        cursor.execute(
            """
            SELECT DISTINCT p.name
            FROM UserRole ur
            INNER JOIN RolePermission rp ON ur.role_id = rp.role_id
            INNER JOIN Permission p ON rp.permission_id = p.permission_id
            WHERE ur.user_id = ?
            """,
            (user_id,),
        )
        permissions = [r.name for r in cursor.fetchall()]

        return CurrentUserSchema(
            user_id=row.user_id,
            username=row.username,
            is_active=row.is_active,
            roles=roles,
            permissions=permissions,
        )


def require_permission(permission_name: str):

    def checker(
        current_user: CurrentUserSchema = Depends(get_current_user),
    ) -> CurrentUserSchema:

        if permission_name not in current_user.permissions:
            raise Errors.forbidden()

        return current_user

    return checker
