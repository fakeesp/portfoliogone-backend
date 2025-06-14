from typing import Literal

from app.enums.error_type import ErrorType

from .base import BaseExceptionResponse


class AccessErrorResponse(BaseExceptionResponse):
    type: Literal[ErrorType.ACCESS_ERROR] = ErrorType.ACCESS_ERROR
