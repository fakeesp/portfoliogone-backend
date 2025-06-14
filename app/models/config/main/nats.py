from .base import BaseSettings


class NatsConfig(BaseSettings, env_prefix="NATS_"):
    username: str
    password: str
    host: str
    port: int

    def build_dsn(self) -> str:
        return f"nats://{self.username}:{self.password}@{self.host}:{self.port}"
