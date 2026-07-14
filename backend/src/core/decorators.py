import functools

from pyodbc import Error

from src.core.exceptions import ExceptionFactory


def handle_db_errors(message: str):
    """
    Wraps a service method so any unexpected pyodbc.Error becomes a
    clean 500 AppException, without repeating try/except in every
    single service method.

    Intentional business exceptions (Errors.user_not_found(), )
    are AppException/HTTPException instances, not pyodbc.Error, so
    they propagate untouched — this decorator never swallows them.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Error:
                raise ExceptionFactory.server_error(message)

        return wrapper

    return decorator
