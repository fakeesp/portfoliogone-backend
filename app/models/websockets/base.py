from pydantic import BaseModel

from app.enums.ws_update_type import WSUpdateType


class WebSocketUpdate(BaseModel):
    type: WSUpdateType
