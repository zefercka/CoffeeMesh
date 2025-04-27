from fastapi import status, HTTPException


class OrderNotFoundError(Exception):
    pass

class APIIntegrationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

class InvalidActionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )

class ExternalServiceUnavailableError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="External service is temporarily unavailable",
        )


class UnauthorizedError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class BadRequestError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )