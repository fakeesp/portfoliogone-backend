from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.sql.game import Game

from .base import BaseRepository


# noinspection PyTypeChecker
class GamesRepository(BaseRepository):
    async def get(self, game_id: int) -> Optional[Game]:
        return await self._get(Game, Game.id == game_id)

    async def get_last(self, load_bids: bool = True) -> Optional[Game]:
        query = select(Game).order_by(Game.id.desc()).limit(1)
        if load_bids:
            query = query.options(joinedload(Game.bids))
        result = await self._session.scalar(query)
        return result
