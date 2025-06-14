import asyncio
from typing import Optional

from fastapi.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.enums.ws_session_type import WebSocketSessionType

from ..models.websockets.base import WebSocketUpdate
from ..utils import mjson


class WebSocketManager:
    _websockets: dict[WebSocketSessionType, dict[str, dict[str, WebSocket]]]
    # session_type
    # wallet or random
    # random_id for multi tabs (random generated)

    def __init__(self) -> None:
        self._websockets = {}

    async def add_websocket(
        self,
        session_type: WebSocketSessionType,
        key: str,
        websocket_id: str,
        websocket: WebSocket,
    ) -> None:
        __websockets: dict[str, dict[str, WebSocket]] = self._websockets.setdefault(
            session_type, {}
        )
        __websockets.setdefault(key, {})
        __websockets[key][websocket_id] = websocket

    def get_websocket(
        self,
        session_type: WebSocketSessionType,
        key: str,
        websocket_id: str,
    ) -> Optional[WebSocket]:
        return self._websockets[session_type].get(key, {}).get(websocket_id)

    async def remove_websocket(
        self,
        session_type: WebSocketSessionType,
        key: str,
        websocket_id: str,
        finish_connection: bool = False,
    ) -> None:
        if key not in self._websockets.setdefault(session_type, {}):
            return
        websocket: WebSocket = self._websockets[session_type].setdefault(key, {}).pop(websocket_id)
        if websocket is not None and finish_connection:
            await websocket.close()

    async def send_text(
        self,
        session_type: WebSocketSessionType,
        key: str,
        websocket_id: str,
        text: str,
    ) -> None:
        if key not in self._websockets.setdefault(session_type, {}):
            return
        websocket = self._websockets[session_type].setdefault(key, {}).get(websocket_id)
        if websocket is None:
            return
        try:
            await websocket.send_text(data=text)
        except WebSocketDisconnect:
            await self.remove_websocket(
                session_type=session_type,
                key=key,
                websocket_id=websocket_id,
            )

    async def send_update(
        self,
        session_type: WebSocketSessionType,
        key: str,
        websocket_id: str,
        update: WebSocketUpdate,
    ) -> None:
        await self.send_text(
            session_type=session_type,
            key=key,
            websocket_id=websocket_id,
            text=mjson.dump_model(model=update),
        )

    async def broadcast_update(
        self,
        *,
        session_type: WebSocketSessionType,
        update: WebSocketUpdate,
    ) -> None:
        if not self._websockets.get(session_type):
            return

        wallet_and_websockets: dict[str, dict[str, WebSocket]] = self._websockets.setdefault(
            session_type, {}
        )

        for user_identifier in wallet_and_websockets:
            if user_identifier not in self._websockets[session_type]:
                return

            text: str = mjson.dump_model(model=update)
            await asyncio.gather(
                *[
                    self.send_text(
                        session_type=session_type,
                        key=user_identifier,
                        websocket_id=websocket_id,
                        text=text,
                    )
                    for websocket_id in self._websockets[session_type][user_identifier]
                ]
            )

    async def broadcast_to_all(
        self,
        *,
        update: WebSocketUpdate,
    ) -> None:
        for session_type, user_identifier_and_random_data in self._websockets.items():
            for user_identifier, websocket_ids in user_identifier_and_random_data.items():
                await asyncio.gather(
                    *[
                        self.send_text(
                            session_type=session_type,
                            key=user_identifier,
                            websocket_id=websocket_id,
                            text=mjson.dump_model(model=update),
                        )
                        for websocket_id in websocket_ids
                    ]
                )
