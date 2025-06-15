from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.game_phase import GamePhase
from app.models.sql.base import Base
from app.models.sql.mixins.timestamp import TimestampMixin
from app.types import Int64

if TYPE_CHECKING:
    from app.models.sql.bid import Bid


class Game(Base, TimestampMixin):
    __tablename__ = "games"

    id: Mapped[Int64] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )

    phase: Mapped[GamePhase] = mapped_column(nullable=False)

    start_eth_price_usdt: Mapped[int] = mapped_column(nullable=False)

    bids: Mapped[list[Bid]] = relationship(
        back_populates="game",
        cascade="all, delete, delete-orphan",
    )
