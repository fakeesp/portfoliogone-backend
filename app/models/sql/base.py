from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Callable, Optional, Self

from pydantic import BaseModel
from sqlalchemy import (
    ARRAY,
    DECIMAL,
    BigInteger,
    DateTime,
    Dialect,
    Enum,
    Integer,
    Interval,
    SmallInteger,
    String,
    TypeDecorator,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, registry
from sqlalchemy.sql.type_api import _T

from app.enums.game_phase import GamePhase
from app.types import (
    DictStrAny,
    DictStrDecimal,
    Int16,
    Int32,
    Int64,
    ListDictStrAny,
    ListInt,
    ListStr,
)
from app.utils import mjson


class JSONMapper(TypeDecorator[JSONB]):
    impl = JSONB

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if not isinstance(value, str):
            return mjson.encode(value)
        return value

    def process_result_value(self, value: Optional[Any], dialect: Dialect) -> Any:
        if not isinstance(value, str):
            return value
        return mjson.decode(value)


class Base(DeclarativeBase):
    __key_builder__: dict[str, Callable[[Any], Any]]

    registry = registry(
        type_annotation_map={
            Int16: SmallInteger,
            Int32: Integer,
            Int64: BigInteger,
            Decimal: DECIMAL,
            DictStrDecimal: JSONMapper,
            DictStrAny: JSONMapper,
            ListDictStrAny: ARRAY(JSONMapper),
            ListInt: ARRAY(BigInteger),
            ListStr: ARRAY(String),
            datetime: DateTime(timezone=True),
            timedelta: Interval(),
            GamePhase: Enum(GamePhase),
        }
    )

    @classmethod
    def from_pydantic(cls, data: BaseModel) -> Self:
        return cls(**data.model_dump())
