from typing import Literal

from app.enums.error_type import ErrorType

from .base import BaseExceptionResponse


class InvalidAmountResponse(BaseExceptionResponse):
    type: Literal[ErrorType.INVALID_AMOUNT] = ErrorType.INVALID_AMOUNT
