import asyncio
import json
from typing import Any

from fastapi import FastAPI
from redis.asyncio import Redis

from app.enums.ws_session_type import WebSocketSessionType
from app.models.websockets.base import WebSocketUpdate
from app.services.websockets import WebSocketManager

REDIS_CHANNEL: str = "ws_updates"


async def dragonfly_pubsub_listener(app: FastAPI) -> None:
    redis: Redis = app.state.dragonfly.client
    ws_manager: WebSocketManager = app.state.ws_manager
    pubsub = redis.pubsub()
    await pubsub.subscribe(REDIS_CHANNEL)
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data: dict[str, Any] = json.loads(message["data"])
                # expects: {"session_type": ..., "key": ..., "websocket_id": ..., "update": {...}}
                await ws_manager.send_update(
                    session_type=WebSocketSessionType(data["session_type"]),
                    key=str(data["key"]),
                    websocket_id=str(data["websocket_id"]),
                    update=(
                        WebSocketUpdate.parse_raw(data["update"])
                        if isinstance(data["update"], str)
                        else WebSocketUpdate.parse_obj(data["update"])
                    ),
                )
    finally:
        await pubsub.unsubscribe(REDIS_CHANNEL)
        await pubsub.close()


def start_dragonfly_listener_task(app: FastAPI) -> None:
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.create_task(dragonfly_pubsub_listener(app))
