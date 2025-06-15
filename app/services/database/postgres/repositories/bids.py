from typing import Optional

from app.models.sql.bid import Bid

from .base import BaseRepository


# noinspection PyTypeChecker
class BidsRepository(BaseRepository):
    async def get_by_game(self, game_id: int) -> list[Bid]:
        return await self._get_all(Bid, Bid.game_id == game_id)

    async def get_by_user_and_game(
        self,
        user_wallet: str,
        game_id: int,
    ) -> list[Bid]:
        return await self._get_all(
            Bid,
            Bid.user_wallet == user_wallet,
            Bid.game_id == game_id,
        )

    async def delete_by_id(self, bid_id: int) -> bool:
        return await self._delete(Bid, Bid.id == bid_id)

    async def get_by_signed_transaction(
        self,
        signed_transaction: str,
    ) -> Optional[Bid]:
        return await self._get(
            Bid,
            Bid.signed_transaction == signed_transaction,
        )
