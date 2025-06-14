from datetime import timezone
from pathlib import Path
from typing import Final

ROOT_DIR: Final[Path] = Path().parent
ASSETS_SOURCE_DIR: Final[Path] = ROOT_DIR / "assets"
MESSAGES_SOURCE_DIR: Final[Path] = ASSETS_SOURCE_DIR / "telegram"

DEFAULT_LOCALE: Final[str] = "en"
TIMEZONE: Final[timezone] = timezone.utc
