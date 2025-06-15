from datetime import timedelta

from pydantic import SecretStr

from app.models.config.main.base import BaseSettings


class JWTConfig(BaseSettings, env_prefix="JWT_"):
    secret: SecretStr
    algorithm: str
    lifetime_in_seconds: int

    @property
    def lifetime(self) -> timedelta:
        return timedelta(seconds=self.lifetime_in_seconds)
