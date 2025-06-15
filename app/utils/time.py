from datetime import datetime
from typing import Any, Optional

from app.const import TIMEZONE


def datetime_now() -> datetime:
    return datetime.now(tz=TIMEZONE)


def cron(
    minute: Optional[int | str] = None,
    hour: Optional[int | str] = None,
    day: Optional[int | str] = None,
    month: Optional[int | str] = None,
    weekday: Optional[int | str] = None,
) -> list[dict[str, Any]]:
    units: list[str] = [
        str(unit) if unit is not None else "*" for unit in [minute, hour, day, month, weekday]
    ]
    return [{"cron": " ".join(units)}]
