from datetime import timedelta
from decimal import Decimal

from pydantic import BaseModel


class StagesDuration(BaseModel):
    bids: timedelta
    signing: timedelta
    reveal: timedelta


class GameSettings(BaseModel):
    stages_duration: StagesDuration
    fee: Decimal
