from pydantic import SecretStr
from sqlalchemy import URL

from .base import BaseSettings


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    db: str
    password: SecretStr
    port: int
    user: str
    data: str

    def build_dsn(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )
