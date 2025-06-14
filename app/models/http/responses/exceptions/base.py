from app.enums.error_type import ErrorType

from ..base import BaseResponse


class BaseExceptionResponse(BaseResponse):
    ok: bool = False
    type: ErrorType = ErrorType.ANY
