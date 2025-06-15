from typing import Final

from fastapi import APIRouter

from . import authorize

router: Final[APIRouter] = APIRouter()
router.include_router(authorize.router)
