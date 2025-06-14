from pydantic_settings import SettingsConfigDict

from app.models.config.assets.game import GameSettings
from app.utils.yaml import YAMLSettings, find_assets_sources


class Assets(YAMLSettings):
    game_settings: GameSettings

    model_config = SettingsConfigDict(
        yaml_file_encoding="utf-8",
        yaml_file=find_assets_sources(),
    )
