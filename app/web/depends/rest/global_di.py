from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, AsyncGenerator, TypeAlias

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.requests import Request
from stollen.session.aiohttp import AiohttpSession

from app.models.config import AppConfig, Assets
from app.services.database import DragonflyRepository, Repository, SQLSessionContext
from app.services.websockets import WebSocketManager


@dataclass
class DependenciesContext:
    dragonfly: DragonflyRepository
    assets: Assets
    ws_manager: WebSocketManager
    app_config: AppConfig
    stollen_session: AiohttpSession


async def get_repository(request: Request) -> AsyncGenerator[Repository, None]:
    if getattr(request.state, "repository", None) is not None:
        yield request.state.repository

    pool: async_sessionmaker[AsyncSession] = request.app.state.session_pool
    async with SQLSessionContext(session_pool=pool) as (repository, uow):
        request.state.repository = repository
        request.state.uow = uow
        yield repository


async def get_dragonfly_repository(request: Request) -> AsyncGenerator[DragonflyRepository, None]:
    yield request.app.state.dragonfly


async def get_assets(request: Request) -> AsyncGenerator[Assets, None]:
    yield request.app.state.assets


async def get_ws_manager(request: Request) -> AsyncGenerator[WebSocketManager, None]:
    yield request.app.state.ws_manager


async def get_app_config(request: Request) -> AsyncGenerator[AppConfig, None]:
    yield request.app.state.app_config


async def get_stollen_session(request: Request) -> AsyncGenerator[AiohttpSession, None]:
    yield request.app.state.stollen_session


async def get_depends_context(request: Request) -> AsyncGenerator[DependenciesContext, None]:
    yield DependenciesContext(
        dragonfly=request.app.state.redis,
        assets=request.app.state.assets,
        ws_manager=request.app.state.ws_manager,
        app_config=request.app.state.app_config,
        stollen_session=request.app.state.stollen_session,
    )


DI_Repository: TypeAlias = Annotated[Repository, Depends(get_repository)]
DI_AppConfig: TypeAlias = Annotated[AppConfig, Depends(get_app_config)]
DI_DragonflyRepository: TypeAlias = Annotated[
    DragonflyRepository, Depends(get_dragonfly_repository)
]
DI_Assets: TypeAlias = Annotated[Assets, Depends(get_assets)]
DI_WSManager: TypeAlias = Annotated[WebSocketManager, Depends(get_ws_manager)]
DI_StollenSession: TypeAlias = Annotated[AiohttpSession, Depends(get_stollen_session)]
DI_DependenciesContext: TypeAlias = Annotated[DependenciesContext, Depends(get_depends_context)]
