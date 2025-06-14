from enum import StrEnum, auto


class WebSocketSessionType(StrEnum):
    UNAUTHORIZED = auto()
    AUTHORIZED = auto()
