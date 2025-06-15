from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.web.websockets.df_pubsub import start_dragonfly_listener_task


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    start_dragonfly_listener_task(app)
    yield
    await app.state.stollen_session.close()
