from pydantic import BaseModel

from .dragonfly import Dragonfly
from .jwt import JWTConfig
from .nats import NatsConfig
from .postgres import PostgresConfig
from .server import ServerConfig


class AppConfig(BaseModel):
    server: ServerConfig
    postgres: PostgresConfig
    dragonfly: Dragonfly
    nats: NatsConfig
    jwt: JWTConfig
