from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.game_phase import GamePhase


class GameStats(BaseModel):
    total_short_bids_amount: Decimal = Field(
        description="Total USDC amount of short bids in the game"
    )
    total_zero_bids_amount: Decimal = Field(
        description="Total USDC amount of zero bids in the game"
    )
    total_long_bids_amount: Decimal = Field(
        description="Total USDC amount of long bids in the game"
    )

    total_count_bids: int = Field(description="Total count of bids in the game")


class GameInfo(BaseModel):
    game_id: int = Field(description="Unique identifier of the game")
    phase: GamePhase = Field(description="Current phase of the game")
    start_eth_price_usdc: Decimal = Field(
        description="Starting ETH price in USDC at the beginning of the game"
    )

    current_eth_price_usdc: Decimal = Field(
        description="Current ETH price in USDC at the time of the game"
    )

    current_phase_start_time: datetime = Field(description="Time when the current phase started")
    stats: GameStats = Field(description="Game statistics including total bid amounts and counts")

    started_at: datetime = Field(description="Time when the game started")
    ended_at: Optional[datetime] = Field(
        description="Time when the game ended, None if the game is still ongoing",
    )
