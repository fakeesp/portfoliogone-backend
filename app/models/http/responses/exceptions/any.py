from typing import Any, Literal

from app.enums.error_type import ErrorType

from .base import BaseExceptionResponse


class AnyErrorResponse(BaseExceptionResponse):
    type: Literal[ErrorType.ANY] = ErrorType.ANY
    message: Any
