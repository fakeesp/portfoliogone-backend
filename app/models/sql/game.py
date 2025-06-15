from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util import greenlet_spawn

from app.enums.game_phase import GamePhase
from app.models.dto.game import GameStats
from app.models.sql.base import Base
from app.models.sql.mixins.timestamp import TimestampMixin
from app.types import Int64
from app.utils.time import datetime_now

if TYPE_CHECKING:
    from app.models.sql.bid import Bid


class Game(Base, TimestampMixin):
    __tablename__ = "games"

    id: Mapped[Int64] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )

    phase: Mapped[GamePhase] = mapped_column(nullable=False, default=GamePhase.BIDDING)
    start_eth_price_usdc: Mapped[Decimal] = mapped_column(nullable=False)

    current_phase_start_time: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime_now,
    )

    bids: Mapped[list[Bid]] = relationship(
        back_populates="game",
        cascade="all, delete, delete-orphan",
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    async def get_bids(self) -> list[Bid]:
        return await greenlet_spawn(lambda: self.bids)

    async def get_stats(self) -> GameStats:
        await self.get_bids()
        return GameStats(
            total_short_bids_amount=sum(
                (bid.amount for bid in self.bids if bid.is_short()), Decimal(0)
            ),
            total_zero_bids_amount=sum(
                (bid.amount for bid in self.bids if bid.is_zero()), Decimal(0)
            ),
            total_long_bids_amount=sum(
                (bid.amount for bid in self.bids if bid.is_long()), Decimal(0)
            ),
            total_count_bids=len(self.bids),
        )
