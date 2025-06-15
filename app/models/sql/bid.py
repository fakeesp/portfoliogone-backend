from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.sql.base import Base
from app.models.sql.mixins.timestamp import TimestampMixin
from app.types import Int64

if TYPE_CHECKING:
    from app.models.sql.game import Game


class Bid(Base, TimestampMixin):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    user_wallet: Mapped[str] = mapped_column(
        ForeignKey("users.wallet", ondelete="CASCADE"), nullable=False
    )
    game_id: Mapped[Int64] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"), nullable=False
    )

    bid_amount: Mapped[Decimal] = mapped_column(nullable=False)
    has_transaction: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    game: Mapped[Game] = relationship(back_populates="bids")
