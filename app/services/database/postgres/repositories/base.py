from __future__ import annotations

from typing import Any, Optional, TypeVar, cast

from sqlalchemy import ColumnElement, ColumnExpressionArgument, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..uow import UoW

T = TypeVar("T", bound=Any)


class BaseRepository:
    _session: AsyncSession
    uow: UoW

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.uow = UoW(session=session)

    async def _get(
        self,
        model: type[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> Optional[T]:
        return cast(Optional[T], await self._session.scalar(select(model).where(*conditions)))

    async def _get_all(
        self,
        model: type[T],
        *conditions: ColumnElement[Any],
    ) -> list[T]:
        result = await self._session.execute(select(model).where(*conditions))
        return list(result.scalars().all())

    async def _get_many(
        self,
        model: type[T],
        limit: int,
        offset: int,
        *conditions: ColumnElement[bool],
    ) -> list[T]:
        result = await self._session.execute(
            select(model).where(*conditions).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    # noinspection PyTypeChecker
    async def _delete(
        self,
        model: type[T],
        *clauses: ColumnExpressionArgument[bool],
    ) -> bool:
        result = await self._session.execute(delete(model).where(*clauses))
        await self._session.commit()
        return result.rowcount > 0

    async def _get_count(
        self,
        *conditions: ColumnElement[bool],
    ) -> int:
        result: Optional[int] = cast(
            Optional[int],
            await self._session.scalar(select(func.count()).where(*conditions)),
        )
        return result or 0
