import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from taskiq import TaskiqDepends, TaskiqState

from app.controllers.game import GameController
from app.models.config.assets.main import Assets
from app.services.database.dragonfly.repository import DragonflyRepository
from app.services.database.postgres.context import SQLSessionContext
from app.services.scheduler import broker
from app.utils.time import cron


@broker.task(schedule=cron(minute="*"))
async def manage_game(state: TaskiqState = TaskiqDepends()) -> None:
    session_pool: async_sessionmaker[AsyncSession] = state.session_pool
    dragonfly: DragonflyRepository = state.dragonfly
    stollen_session = state.stollen_session
    assets: Assets = state.assets

    async with SQLSessionContext(session_pool=session_pool) as (repository, uow):
        game_controller: GameController = GameController(
            repository=repository,
            dragonfly=dragonfly,
            stollen_session=stollen_session,
            assets=assets,
        )

        for _ in range(1, 12):
            await game_controller.update_game()
            await asyncio.sleep(5)
