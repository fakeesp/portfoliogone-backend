from typing import Literal

from app.enums.error_type import ErrorType

from .base import BaseExceptionResponse


class TimeoutErrorResponse(BaseExceptionResponse):
    type: Literal[ErrorType.TIMEOUT] = ErrorType.TIMEOUT
