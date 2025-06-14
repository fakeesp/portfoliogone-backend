from typing import Literal

from app.enums.error_type import ErrorType

from .base import BaseExceptionResponse


class NotFoundResponse(BaseExceptionResponse):
    type: Literal[ErrorType.NOT_FOUND] = ErrorType.NOT_FOUND
