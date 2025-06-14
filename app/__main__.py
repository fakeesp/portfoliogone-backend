from fastapi import FastAPI

from .factory.app import create_app
from .factory.config import create_app_config
from .models.config import AppConfig
from .runner import run_app


def main() -> None:
    config: AppConfig = create_app_config()
    app: FastAPI = create_app(config=config)
    return run_app(app=app, config=config)


if __name__ == "__main__":
    main()
