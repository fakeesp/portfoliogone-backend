import asyncio
import json
import uuid
from typing import Any, Callable, Coroutine, Dict, List, Optional

import websockets
from websockets.legacy.client import WebSocketClientProtocol

MessageHandlerType = Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]


class ClearnetClient:
    def __init__(self, url: str, timeout: float = 10.0) -> None:
        self.url: str = url
        self.timeout: float = timeout
        self._pending: Dict[str, asyncio.Future[Dict[str, Any]]] = {}
        self._ws: Optional[WebSocketClientProtocol] = None
        self._receiver_task: Optional[asyncio.Task[None]] = None
        self._connected: asyncio.Event = asyncio.Event()
        self._message_handlers: List[MessageHandlerType] = []

    async def connect(self) -> None:
        self._ws = await websockets.connect(self.url)
        self._connected.set()
        self._receiver_task = asyncio.create_task(self._receiver())

    async def close(self) -> None:
        if self._ws:
            await self._ws.close()
        if self._receiver_task:
            self._receiver_task.cancel()
        for fut in self._pending.values():
            if not fut.done():
                fut.set_exception(Exception("WebSocket closed"))
        self._pending.clear()

    async def _receiver(self) -> None:
        if self._ws is None:
            raise RuntimeError("WebSocket is not connected")
        try:
            async for msg in self._ws:
                data: Dict[str, Any] = json.loads(msg)
                msg_id: Optional[str] = data.get("id")
                if msg_id and msg_id in self._pending:
                    fut: asyncio.Future[Dict[str, Any]] = self._pending.pop(msg_id)
                    fut.set_result(data)
                else:
                    for handler in self._message_handlers:
                        asyncio.create_task(handler(data))
        except Exception as e:
            for fut in self._pending.values():
                if not fut.done():
                    fut.set_exception(e)
            self._pending.clear()

    async def request(
        self, method: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        await self._connected.wait()
        msg_id: str = str(uuid.uuid4())
        req: Dict[str, Any] = {"id": msg_id, "method": method, "params": params or {}}
        fut: asyncio.Future[Dict[str, Any]] = asyncio.get_event_loop().create_future()
        self._pending[msg_id] = fut
        if self._ws is None:
            raise RuntimeError("WebSocket is not connected")
        await self._ws.send(json.dumps(req))
        try:
            resp: Dict[str, Any] = await asyncio.wait_for(fut, timeout=self.timeout)
        except asyncio.TimeoutError:
            self._pending.pop(msg_id, None)
            raise TimeoutError(f"Timeout for method {method}")
        return resp

    def on_message(self, callback: MessageHandlerType) -> None:
        self._message_handlers.append(callback)
