from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stollen.requests import RequestSerializer
from stollen.session.aiohttp import AiohttpSession

from app.services.database.clearnet import ClearnetClient

from ..lifespan import lifespan
from ..models.config import AppConfig
from ..models.config.assets.main import Assets
from ..models.websockets.base import WebSocketUpdate
from ..services.websockets import WebSocketManager
from ..utils import mjson
from ..web import rest, websockets
from ..web.exceptions import API_ERRORS, handle_error
from .dragonfly import create_dragonfly
from .session_pool import create_session_pool


def append_additional_schemas(app: FastAPI) -> None:
    from fastapi.openapi.constants import REF_TEMPLATE
    from fastapi.openapi.utils import get_openapi

    if app.openapi_schema:
        return

    # noinspection PyUnresolvedReferences
    openapi_schema: dict[str, Any] = get_openapi(
        title=app.title,
        version=app.version,
        summary=app.summary,
        description=app.description,
        routes=app.routes,
    )
    extras: dict[str, Any] = {
        subclass.__name__: {
            **subclass.model_json_schema(ref_template=REF_TEMPLATE),
            "description": "Websocket event",
        }
        for subclass in WebSocketUpdate.__subclasses__()
    }
    openapi_schema["components"]["schemas"].update(extras)
    app.openapi_schema = openapi_schema


def create_app(config: AppConfig) -> FastAPI:
    app: FastAPI = FastAPI(lifespan=lifespan)

    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(rest.router, prefix="/api")
    app.include_router(websockets.router, prefix="/ws")

    # noinspection PyArgumentList
    app.state.assets = Assets()
    app.state.stollen_session = AiohttpSession(
        serializer=RequestSerializer(
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        timeout=15,
    )
    app.state.ws_manager = WebSocketManager()
    app.state.app_config = config
    app.state.session_pool = create_session_pool(config.postgres.build_dsn())
    app.state.dragonfly = create_dragonfly(config.dragonfly.build_dsn())
    app.state.clearnet = ClearnetClient("wss://clearnode.yellow.com/ws")

    # append_additional_schemas(app)

    for error_type in API_ERRORS:
        app.add_exception_handler(error_type, handle_error)

    return app
