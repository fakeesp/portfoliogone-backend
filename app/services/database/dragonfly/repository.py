from __future__ import annotations

from typing import Any, Optional, TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis
from redis.asyncio.lock import Lock
from redis.typing import ExpiryT

from app.services.database.dragonfly.keys import LockGameBidsKey
from app.utils import mjson
from app.utils.key_builder import StorageKey
from app.utils.mjson import validate_list, validate_raw

T = TypeVar("T", bound=Any)


class DragonflyRepository:
    client: Redis

    def __init__(self, client: Redis) -> None:
        self.client = client

    async def get(self, key: StorageKey, validator: type[T]) -> Optional[T]:
        value: Optional[Any] = await self.client.get(key.pack())
        if value is None:
            return None
        return validate_raw(data=value, validator=validator)

    async def get_many(self, keys: list[StorageKey], validator: type[T]) -> list[T]:
        values: list[Any] = await self.client.mget([key.pack() for key in keys])
        return validate_list(data=values, validator=validator)

    async def set(self, key: StorageKey, value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key.pack(), value=mjson.encode(value), ex=ex)

    async def set_by_str_key(self, key: str, value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key, value=mjson.encode(value), ex=ex)

    async def update_ttl(self, key: str, ex: ExpiryT) -> None:
        await self.client.expire(name=key, time=ex)

    async def delete(self, key: StorageKey) -> None:
        await self.client.delete(key.pack())

    async def close(self) -> None:
        await self.client.aclose(close_connection_pool=True)

    def lock(self, key: StorageKey) -> Lock:
        return self.client.lock(key.pack())

    def lock_bids_by_game(self, game_id: int) -> Lock:
        return self.lock(LockGameBidsKey(game_id=game_id))
