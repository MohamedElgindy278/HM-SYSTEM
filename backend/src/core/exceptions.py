from fastapi import HTTPException, status

# ==========================================================
# ERROR CODES REGISTRY
# ==========================================================


class ErrorCodes:

    # AUTH
    AUTH_INVALID_CREDENTIALS = "AUTH_001"
    AUTH_INVALID_TOKEN = "AUTH_002"
    AUTH_EXPIRED_TOKEN = "AUTH_003"
    AUTH_UNAUTHORIZED = "AUTH_004"
    AUTH_FORBIDDEN = "AUTH_005"
    AUTH_USER_INACTIVE = "AUTH_006"

    # USER
    USER_NOT_FOUND = "USER_001"
    USER_ALREADY_EXISTS = "USER_002"
    USER_EMAIL_ALREADY_EXISTS = "USER_003"

    # DOCTOR
    DOCTOR_NOT_FOUND = "DOCTOR_001"
    DOCTOR_ALREADY_EXISTS = "DOCTOR_002"
    DOCTOR_LICENSE_ALREADY_EXISTS = "DOCTOR_003"

    # DOCTOR SCHEDULE
    DOCTOR_SCHEDULE_NOT_FOUND = "DOCTOR_SCHEDULE_001"
    DOCTOR_SCHEDULE_ALREADY_EXISTS = "DOCTOR_SCHEDULE_002"
    DOCTOR_SCHEDULE_INVALID_DAY = "DOCTOR_SCHEDULE_003"
    DOCTOR_SCHEDULE_INVALID_TIME_RANGE = "DOCTOR_SCHEDULE_004"

    # PATIENT
    PATIENT_NOT_FOUND = "PATIENT_001"
    PATIENT_EXISTS = "PATIENT_002"
    PATIENT_MRN_EXISTS = "PATIENT_003"
    PATIENT_NATIONAL_ID_EXISTS = "PATIENT_004"

    # SYSTEM
    INTERNAL_SERVER_ERROR = "SYSTEM_001"
    CONFLICT = "SYSTEM_002"
    VALIDATION_ERROR = "SYSTEM_003"

    # INSURANCE PROVIDER
    INSURANCE_PROVIDER_NOT_FOUND = "INSURANCE_PROVIDER_001"
    INSURANCE_PROVIDER_ALREADY_EXISTS = "INSURANCE_PROVIDER_002"

    # INSURANCE POLICY
    INSURANCE_POLICY_NOT_FOUND = "INSURANCE_POLICY_001"
    INSURANCE_POLICY_EXISTS = "INSURANCE_POLICY_002"
    PATIENT_HAS_ACTIVE_POLICY = "INSURANCE_POLICY_003"

    # BRANCH
    BRANCH_NOT_FOUND = "BRANCH_001"

    # DEPARTMENT
    DEPARTMENT_NOT_FOUND = "DEPARTMENT_001"
    DEPARTMENT_ALREADY_EXISTS = "DEPARTMENT_002"

    # SPECIALIZATION
    SPECIALTY_NOT_FOUND = "SPECIALTY_001"
    SPECIALTY_ALREADY_EXISTS = "SPECIALTY_002"

    # APPOINTMENT
    APPOINTMENT_NOT_FOUND = "APPOINTMENT_001"
    APPOINTMENT_DOCTOR_NOT_AVAILABLE = "APPOINTMENT_002"
    APPOINTMENT_PATIENT_HAS_APPOINTMENT = "APPOINTMENT_003"
    APPOINTMENT_INVALID_DATE = "APPOINTMENT_004"


# ==========================================================
# BASE EXCEPTION
# ==========================================================


class AppException(HTTPException):

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "status_code": status_code,
                "error_code": error_code,
                "message": message,
            },
        )


# ==========================================================
# EXCEPTION FACTORY
# ==========================================================


class ExceptionFactory:

    @staticmethod
    def not_found(
        error_code: str,
        message: str,
    ):
        return AppException(
            status.HTTP_404_NOT_FOUND,
            error_code,
            message,
        )

    @staticmethod
    def bad_request(
        error_code: str,
        message: str,
    ):
        return AppException(
            status.HTTP_400_BAD_REQUEST,
            error_code,
            message,
        )

    @staticmethod
    def unauthorized(
        error_code: str,
        message: str,
    ):
        return AppException(
            status.HTTP_401_UNAUTHORIZED,
            error_code,
            message,
        )

    @staticmethod
    def forbidden(
        error_code: str,
        message: str,
    ):
        return AppException(
            status.HTTP_403_FORBIDDEN,
            error_code,
            message,
        )

    @staticmethod
    def conflict(
        error_code: str,
        message: str,
    ):
        return AppException(
            status.HTTP_409_CONFLICT,
            error_code,
            message,
        )

    @staticmethod
    def server_error(
        message: str = "Internal server error",
    ):
        return AppException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            ErrorCodes.INTERNAL_SERVER_ERROR,
            message,
        )


# ==========================================================
# PRE-BUILT COMMON ERRORS
# ==========================================================


class Errors:

    # =========================
    # AUTH
    # =========================

    @staticmethod
    def invalid_credentials():
        return ExceptionFactory.unauthorized(
            ErrorCodes.AUTH_INVALID_CREDENTIALS,
            "Invalid username or password",
        )

    @staticmethod
    def inactive_user():
        return ExceptionFactory.forbidden(
            ErrorCodes.AUTH_USER_INACTIVE,
            "User account is inactive",
        )

    @staticmethod
    def invalid_token():
        return ExceptionFactory.unauthorized(
            ErrorCodes.AUTH_INVALID_TOKEN,
            "Invalid token",
        )

    @staticmethod
    def expired_token():
        return ExceptionFactory.unauthorized(
            ErrorCodes.AUTH_EXPIRED_TOKEN,
            "Token has expired",
        )

    @staticmethod
    def unauthorized():
        return ExceptionFactory.unauthorized(
            ErrorCodes.AUTH_UNAUTHORIZED,
            "Authentication required",
        )

    @staticmethod
    def forbidden():
        return ExceptionFactory.forbidden(
            ErrorCodes.AUTH_FORBIDDEN,
            "Access denied",
        )

    # =========================
    # USER
    # =========================

    @staticmethod
    def user_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.USER_NOT_FOUND,
            "User not found",
        )

    @staticmethod
    def user_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.USER_ALREADY_EXISTS,
            "Username already exists",
        )

    @staticmethod
    def email_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.USER_EMAIL_ALREADY_EXISTS,
            "Email already exists",
        )

    # =========================
    # DOCTOR
    # =========================

    @staticmethod
    def doctor_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.DOCTOR_NOT_FOUND,
            "Doctor not found",
        )

    @staticmethod
    def doctor_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.DOCTOR_ALREADY_EXISTS,
            "User is already assigned as a doctor",
        )

    @staticmethod
    def doctor_license_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.DOCTOR_LICENSE_ALREADY_EXISTS,
            "License number already exists",
        )

    # =========================
    # DOCTOR SCHEDULE
    # =========================

    @staticmethod
    def doctor_schedule_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.DOCTOR_SCHEDULE_NOT_FOUND,
            "Doctor schedule not found",
        )

    @staticmethod
    def doctor_schedule_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.DOCTOR_SCHEDULE_ALREADY_EXISTS,
            "Doctor already has a schedule for this day",
        )

    @staticmethod
    def invalid_day_of_week():
        return ExceptionFactory.bad_request(
            ErrorCodes.DOCTOR_SCHEDULE_INVALID_DAY,
            "Invalid day of week",
        )

    @staticmethod
    def invalid_schedule_time():
        return ExceptionFactory.bad_request(
            ErrorCodes.DOCTOR_SCHEDULE_INVALID_TIME_RANGE,
            "Start time must be before end time",
        )

    # =========================
    # PATIENT
    # =========================

    @staticmethod
    def patient_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.PATIENT_NOT_FOUND,
            "Patient not found",
        )

    @staticmethod
    def patient_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.PATIENT_EXISTS,
            "Patient already exists",
        )

    @staticmethod
    def patient_mrn_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.PATIENT_MRN_EXISTS,
            "Medical Record Number (MRN) already exists",
        )

    @staticmethod
    def patient_national_id_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.PATIENT_NATIONAL_ID_EXISTS,
            "National ID already exists",
        )

    # ==========================
    # INSURANCE POLICY
    # ==========================

    @staticmethod
    def insurance_policy_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.INSURANCE_POLICY_NOT_FOUND,
            "Insurance policy not found",
        )

    @staticmethod
    def insurance_policy_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.INSURANCE_POLICY_EXISTS,
            "Insurance policy already exists",
        )

    @staticmethod
    def patient_has_active_policy():
        return ExceptionFactory.conflict(
            ErrorCodes.PATIENT_HAS_ACTIVE_POLICY,
            "Patient already has an active insurance policy",
        )

    # =========================
    # INSURANCE PROVIDER
    # =========================

    @staticmethod
    def insurance_provider_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.INSURANCE_PROVIDER_NOT_FOUND,
            "Insurance provider not found",
        )

    @staticmethod
    def insurance_provider_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.INSURANCE_PROVIDER_ALREADY_EXISTS,
            "Insurance provider already exists",
        )

    # =========================
    # BRANCH
    # =========================

    @staticmethod
    def branch_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.BRANCH_NOT_FOUND,
            "Branch not found",
        )

    # =========================
    # DEPARTMENT
    # =========================

    @staticmethod
    def department_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.DEPARTMENT_NOT_FOUND,
            "Department not found",
        )

    @staticmethod
    def department_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.DEPARTMENT_ALREADY_EXISTS,
            "Department already exists",
        )

    # =========================
    # SPECIALIZATION
    # =========================

    @staticmethod
    def specialty_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.SPECIALTY_NOT_FOUND,
            "Specialization not found",
        )

    @staticmethod
    def specialty_exists():
        return ExceptionFactory.conflict(
            ErrorCodes.SPECIALTY_ALREADY_EXISTS,
            "Specialization already exists",
        )

    # =========================
    # APPOINTMENT
    # =========================

    @staticmethod
    def appointment_not_found():
        return ExceptionFactory.not_found(
            ErrorCodes.APPOINTMENT_NOT_FOUND,
            "Appointment not found",
        )

    @staticmethod
    def doctor_not_available():
        return ExceptionFactory.conflict(
            ErrorCodes.APPOINTMENT_DOCTOR_NOT_AVAILABLE,
            "Doctor is not available at the selected time",
        )

    @staticmethod
    def patient_has_appointment():
        return ExceptionFactory.conflict(
            ErrorCodes.APPOINTMENT_PATIENT_HAS_APPOINTMENT,
            "Patient already has an appointment at the selected time",
        )

    @staticmethod
    def invalid_appointment_date():
        return ExceptionFactory.bad_request(
            ErrorCodes.APPOINTMENT_INVALID_DATE,
            "Appointment date must be in the future",
        )

    # =========================
    # GENERIC
    # =========================

    @staticmethod
    def validation_error(
        message: str,
    ):
        return ExceptionFactory.bad_request(
            ErrorCodes.VALIDATION_ERROR,
            message,
        )

    @staticmethod
    def conflict(
        message: str,
    ):
        return ExceptionFactory.conflict(
            ErrorCodes.CONFLICT,
            message,
        )

    @staticmethod
    def internal_server_error():
        return ExceptionFactory.server_error()
