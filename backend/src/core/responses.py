from fastapi.responses import JSONResponse
from fastapi import status

# ==========================================================
# BASE RESPONSE
# ==========================================================


class AppResponse:

    @staticmethod
    def send(status_code: int, message: str, data=None):
        return JSONResponse(
            status_code=status_code,
            content={
                "status_code": status_code,
                "message": message,
                "data": data,
            },
        )


# ==========================================================
# RESPONSE HELPERS
# ==========================================================


class Responses:

    @staticmethod
    def ok(data=None, message: str = "Success"):
        return AppResponse.send(
            status.HTTP_200_OK,
            message,
            data,
        )

    @staticmethod
    def created(data=None, message: str = "Created successfully"):
        return AppResponse.send(
            status.HTTP_201_CREATED,
            message,
            data,
        )

    @staticmethod
    def accepted(data=None, message: str = "Request accepted"):
        return AppResponse.send(
            status.HTTP_202_ACCEPTED,
            message,
            data,
        )

    @staticmethod
    def deleted(message: str = "Deleted successfully"):
        return AppResponse.send(
            status.HTTP_200_OK,
            message,
            None,
        )
