from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .bids import BidsRepository
from .games import GamesRepository
from .users import UsersRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    users: UsersRepository
    bids: BidsRepository
    games: GamesRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.users = UsersRepository(session=session)
        self.bids = BidsRepository(session=session)
        self.games = GamesRepository(session=session)
