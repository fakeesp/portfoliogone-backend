from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util import greenlet_spawn

from app.enums.bid_type import BidType
from app.models.dto.bid import BidDto
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

    bid_type: Mapped[BidType] = mapped_column(
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(nullable=False)
    signed_transaction: Mapped[Optional[str]] = mapped_column(
        nullable=True,
    )

    game: Mapped[Game] = relationship(back_populates="bids")

    async def get_game(self) -> Game:
        return await greenlet_spawn(lambda: self.game)

    def is_short(self) -> bool:
        return self.bid_type == BidType.SHORT

    def is_zero(self) -> bool:
        return self.bid_type == BidType.ZERO

    def is_long(self) -> bool:
        return self.bid_type == BidType.LONG

    def dto(self) -> BidDto:
        return BidDto(
            id=self.id,
            user_wallet=self.user_wallet,
            game_id=self.game_id,
            bid_type=self.bid_type,
            amount=self.amount,
            signed_transaction=self.signed_transaction,
            created_at=self.created_at,
        )
