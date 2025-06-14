from .base import BaseSettings


class ServerConfig(BaseSettings, env_prefix="SERVER_"):
    port: int
    host: str
