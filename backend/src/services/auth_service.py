from src.config.database import get_pyodbc_connection
from src.config.settings import settings
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.core.security import (
    create_access_token,
    generate_otp,
    generate_refresh_token,
    hash_otp,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from src.schemas.auth_schema import (
    ChangePasswordSchema,
    ForgotPasswordSchema,
    LoginSchema,
    RefreshTokenSchema,
    ResetPasswordSchema,
    TokenResponseSchema,
    VerifyOTPSchema,
)
from src.utils.email_service import EmailService

_DUMMY_HASH = hash_password("dummy-password-for-timing-safety")


class AuthService:

    @staticmethod
    @handle_db_errors("Failed to login")
    def login(login_data: LoginSchema, ip_address: str = None) -> TokenResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT user_id, password_hash, is_active, is_deleted
                FROM [User]
                WHERE username = ?
                """,
                (login_data.username,),
            )
            row = cursor.fetchone()

            stored_hash = (
                row.password_hash if row and not row.is_deleted else _DUMMY_HASH
            )
            password_valid = verify_password(login_data.password, stored_hash)

            if not row or row.is_deleted or not password_valid:
                raise Errors.invalid_credentials()

            if not row.is_active:
                raise Errors.inactive_user()

            expire_days = (
                settings.REFRESH_TOKEN_EXPIRE_DAYS if login_data.remember_me else 1
            )

            access_token = create_access_token(row.user_id)
            refresh_token = generate_refresh_token()

            cursor.execute(
                """
                INSERT INTO [RefreshToken] (user_id, token_hash, expires_at, ip_address)
                VALUES (?, ?, DATEADD(DAY, ?, GETDATE()), ?)
                """,
                (
                    row.user_id,
                    hash_refresh_token(refresh_token),
                    expire_days,
                    ip_address,
                ),
            )
            conn.commit()

            return TokenResponseSchema(
                access_token=access_token, refresh_token=refresh_token
            )

    @staticmethod
    @handle_db_errors("Failed to refresh token")
    def refresh(refresh_data: RefreshTokenSchema) -> TokenResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            token_hash = hash_refresh_token(refresh_data.refresh_token)

            cursor.execute(
                """
                SELECT token_id, user_id
                FROM [RefreshToken]
                WHERE token_hash = ?
                AND revoked = 0
                AND expires_at > GETDATE()
                """,
                (token_hash,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.invalid_token()

            cursor.execute(
                "SELECT is_active, is_deleted FROM [User] WHERE user_id = ?",
                (row.user_id,),
            )
            user_row = cursor.fetchone()

            if not user_row or user_row.is_deleted:
                raise Errors.invalid_token()

            if not user_row.is_active:
                raise Errors.inactive_user()

            cursor.execute(
                "UPDATE [RefreshToken] SET revoked = 1, revoked_at = GETDATE() WHERE token_id = ?",
                (row.token_id,),
            )

            access_token = create_access_token(row.user_id)
            new_refresh_token = generate_refresh_token()

            cursor.execute(
                """
                INSERT INTO [RefreshToken] (user_id, token_hash, expires_at)
                VALUES (?, ?, DATEADD(DAY, ?, GETDATE()))
                """,
                (
                    row.user_id,
                    hash_refresh_token(new_refresh_token),
                    settings.REFRESH_TOKEN_EXPIRE_DAYS,
                ),
            )
            conn.commit()

            return TokenResponseSchema(
                access_token=access_token, refresh_token=new_refresh_token
            )

    @staticmethod
    @handle_db_errors("Failed to logout")
    def logout(refresh_data: RefreshTokenSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            token_hash = hash_refresh_token(refresh_data.refresh_token)

            cursor.execute(
                "UPDATE [RefreshToken] SET revoked = 1, revoked_at = GETDATE() WHERE token_hash = ? AND revoked = 0",
                (token_hash,),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to change password")
    def change_password(user_id: int, data: ChangePasswordSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT password_hash FROM [User] WHERE user_id = ? AND is_deleted = 0",
                (user_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.user_not_found()

            if not verify_password(data.old_password, row.password_hash):
                raise Errors.invalid_credentials()

            cursor.execute(
                "UPDATE [User] SET password_hash = ?, updated_at = GETDATE() WHERE user_id = ?",
                (hash_password(data.new_password), user_id),
            )

            cursor.execute(
                "UPDATE [RefreshToken] SET revoked = 1, revoked_at = GETDATE() WHERE user_id = ? AND revoked = 0",
                (user_id,),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to process forgot password")
    def forgot_password(forgot_data: ForgotPasswordSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT user_id, is_active, is_deleted FROM [User] WHERE email = ?",
                (forgot_data.email,),
            )
            row = cursor.fetchone()

            if not row or row.is_deleted or not row.is_active:
                return

            cursor.execute(
                "DELETE FROM PasswordResetOTP WHERE user_id = ? AND verified = 0",
                (row.user_id,),
            )

            otp = generate_otp()
            otp_hash = hash_otp(otp)

            cursor.execute(
                """
                INSERT INTO PasswordResetOTP (user_id, otp_hash, expires_at)
                VALUES (?, ?, DATEADD(MINUTE, 5, GETDATE()))
                """,
                (row.user_id, otp_hash),
            )
            conn.commit()

            EmailService.send_email(
                to_email=forgot_data.email,
                subject="Password Reset OTP",
                body=f"""
                    Hello,

                    Your One-Time Password (OTP) is:

                    {otp}

                    This OTP will expire in 5 minutes and can only be used once.

                    If you did not request a password reset, please ignore this email.

                    Regards,
                    MedCore HMS
                    """,
            )

    @staticmethod
    @handle_db_errors("Failed to verify OTP")
    def verify_otp(otp_data: VerifyOTPSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT user_id FROM [User] WHERE email = ? AND is_deleted = 0",
                (otp_data.email,),
            )
            user = cursor.fetchone()

            if not user:
                raise Errors.invalid_otp()

            cursor.execute(
                """
                SELECT otp_id, otp_hash
                FROM PasswordResetOTP
                WHERE user_id = ?
                AND verified = 0
                AND expires_at > GETDATE()
                """,
                (user.user_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.invalid_otp()

            # Single attempt: a wrong guess burns the OTP immediately,
            # the user has to request a fresh one
            if row.otp_hash != hash_otp(otp_data.otp):
                cursor.execute(
                    "DELETE FROM PasswordResetOTP WHERE otp_id = ?", (row.otp_id,)
                )
                conn.commit()
                raise Errors.invalid_otp()

            cursor.execute(
                "UPDATE PasswordResetOTP SET verified = 1 WHERE otp_id = ?",
                (row.otp_id,),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to reset password")
    def reset_password(data: ResetPasswordSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT user_id FROM [User] WHERE email = ? AND is_deleted = 0",
                (data.email,),
            )
            user = cursor.fetchone()

            if not user:
                raise Errors.user_not_found()

            cursor.execute(
                """
                SELECT otp_id
                FROM PasswordResetOTP
                WHERE user_id = ?
                AND verified = 1
                AND expires_at > GETDATE()
                """,
                (user.user_id,),
            )
            otp = cursor.fetchone()

            if not otp:
                raise Errors.invalid_otp()

            cursor.execute(
                "UPDATE [User] SET password_hash = ?, updated_at = GETDATE() WHERE user_id = ?",
                (hash_password(data.new_password), user.user_id),
            )

            cursor.execute(
                "DELETE FROM PasswordResetOTP WHERE user_id = ?",
                (user.user_id,),
            )

            cursor.execute(
                "UPDATE [RefreshToken] SET revoked = 1, revoked_at = GETDATE() WHERE user_id = ? AND revoked = 0",
                (user.user_id,),
            )
            conn.commit()
