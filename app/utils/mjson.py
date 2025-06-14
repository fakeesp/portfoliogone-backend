from typing import Any, Callable, Final, TypeVar

from msgspec.json import Decoder, Encoder
from pydantic import BaseModel, TypeAdapter

decode: Final[Callable[..., Any]] = Decoder[dict[str, Any]]().decode
bytes_encode: Final[Callable[..., bytes]] = Encoder().encode

T = TypeVar("T", bound=Any)


def encode(obj: Any) -> str:
    data: bytes = bytes_encode(obj)
    return data.decode()


def dump_model(model: BaseModel, **dump_kwargs: Any) -> str:
    return encode(model.model_dump(**dump_kwargs))


def get_adapter(validator: type[T]) -> TypeAdapter[T]:
    return TypeAdapter[T](validator)


def validate_raw(data: str | bytes, validator: type[T]) -> T:
    return TypeAdapter[T](validator).validate_python(decode(data))


def validate_list(data: list[Any], validator: type[T]) -> list[T]:
    list_validator: type[list[T]] = list[validator]  # type: ignore
    return TypeAdapter[list[T]](list_validator).validate_python(
        [decode(item) for item in data if item is not None]
    )
