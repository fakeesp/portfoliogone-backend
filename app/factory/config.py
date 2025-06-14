from ..models.config.main import (
    AppConfig,
    Dragonfly,
    NatsConfig,
    PostgresConfig,
    ServerConfig,
)


def create_app_config() -> AppConfig:
    return AppConfig(
        server=ServerConfig(),
        postgres=PostgresConfig(),
        dragonfly=Dragonfly(),
        nats=NatsConfig(),
    )
