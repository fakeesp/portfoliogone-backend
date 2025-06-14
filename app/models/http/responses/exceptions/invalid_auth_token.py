from typing import Literal

from app.enums.error_type import ErrorType

from .base import BaseExceptionResponse


class InvalidAuthTokenResponse(BaseExceptionResponse):
    type: Literal[ErrorType.INVALID_AUTH_TOKEN] = ErrorType.INVALID_AUTH_TOKEN
