from typing import Final

from fastapi import APIRouter

# from . import get_game_stats

router: Final[APIRouter] = APIRouter(prefix="/bids", tags=["bids"])
# router.include_router(get_game_stats.router)
