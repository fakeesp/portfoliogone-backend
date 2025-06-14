from .base import BaseResponse


class BoolResponse(BaseResponse):
    data: bool = True
