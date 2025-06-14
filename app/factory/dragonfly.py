from __future__ import annotations

from redis.asyncio import ConnectionPool, Redis

from app.services.database import DragonflyRepository


def create_dragonfly(url: str) -> DragonflyRepository:
    return DragonflyRepository(client=Redis(connection_pool=ConnectionPool.from_url(url=url)))
