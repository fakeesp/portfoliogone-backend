from typing import Literal
from app.enums.ws_update_type import WSUpdateType
from app.models.websockets.base import WebSocketUpdate


class GameUpdate(WebSocketUpdate):
    type: Literal[WSUpdateType.GAME_UPDATE] = WSUpdateType.GAME_UPDATE
    short_count: int
    zero_count: int
    long_count: int
