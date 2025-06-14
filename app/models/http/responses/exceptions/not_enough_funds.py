from typing import Literal

from app.enums.error_type import ErrorType

from .base import BaseExceptionResponse


class NotEnoughFundsResponse(BaseExceptionResponse):
    type: Literal[ErrorType.NOT_ENOUGH_FUNDS] = ErrorType.NOT_ENOUGH_FUNDS
