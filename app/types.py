from decimal import Decimal
from typing import Annotated, Any
from uuid import UUID

# Data types
Int16 = Annotated[int, 16]
Int32 = Annotated[int, 32]
Int64 = Annotated[int, 64]
DictStrAny = dict[str, Any]
DictStrDecimal = dict[str, Decimal]
ListInt = list[Int64]
ListStr = list[str]
TextMap = dict[str, str]
ListDictStrAny = list[DictStrAny]
DictUUIDStrDecimal = dict[UUID, DictStrDecimal]
