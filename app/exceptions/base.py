from typing import Optional

from stollen.utils.text import camel_to_snake


class ControllerError(Exception):
    message: str

    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = camel_to_snake(self.__class__.__name__).upper()
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class NotFoundError(ControllerError):
    pass
