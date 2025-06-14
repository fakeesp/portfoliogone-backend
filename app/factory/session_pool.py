from __future__ import annotations

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.utils import mjson


def create_session_pool(dsn: URL) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(url=dsn, json_serializer=mjson.encode)
    return async_sessionmaker(engine, expire_on_commit=False)
