from typing import Optional

from app.models.sql.user import User

from .base import BaseRepository


# noinspection PyTypeChecker
class UsersRepository(BaseRepository):
    async def get(self, wallet: str) -> Optional[User]:
        return await self._get(User, User.wallet == wallet)
