from contextlib import suppress

import uvicorn
from fastapi import FastAPI

from .models.config.main.app import AppConfig


def run_app(app: FastAPI, config: AppConfig) -> None:
    with suppress(KeyboardInterrupt):
        return uvicorn.run(
            app=app,
            host=config.server.host,
            port=config.server.port,
        )
