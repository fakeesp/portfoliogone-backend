from .base import BaseSettings


class Dragonfly(BaseSettings, env_prefix="DRAGONFLY_"):
    host: str
    port: int
    db: int
    data: str

    def build_dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"
