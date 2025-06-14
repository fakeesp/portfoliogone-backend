from enum import StrEnum, auto


class ErrorType(StrEnum):
    ACCESS_ERROR = auto()
    NOT_FOUND = auto()
    ANY = auto()
    TIMEOUT = auto()
    NOT_ENOUGH_FUNDS = auto()
    INVALID_AUTH_TOKEN = auto()
    INVALID_AMOUNT = auto()
