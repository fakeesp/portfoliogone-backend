from typing import Final

from stollen.session.aiohttp import AiohttpSession
from taskiq import (
    AsyncBroker,
    ScheduleSource,
    TaskiqEvents,
    TaskiqScheduler,
    TaskiqState,
)
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker
from taskiq_redis import RedisScheduleSource

from app.factory.config import create_app_config
from app.factory.dragonfly import create_dragonfly
from app.factory.session_pool import create_session_pool
from app.models.config import AppConfig

config: Final[AppConfig] = create_app_config()
broker: Final[AsyncBroker] = NatsBroker(servers=[config.nats.build_dsn()], queue="bot-tasks")
source: Final[ScheduleSource] = RedisScheduleSource(url=config.dragonfly.build_dsn())
scheduler: Final[TaskiqScheduler] = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker), source],
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    state.config = config
    state.session_pool = create_session_pool(dsn=config.postgres.build_dsn())
    state.dragonfly = create_dragonfly(url=config.dragonfly.build_dsn())
    state.stollen_session = AiohttpSession()
