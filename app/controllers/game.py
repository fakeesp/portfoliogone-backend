from decimal import Decimal
from typing import Optional

from stollen.session.aiohttp import AiohttpSession

from app.enums.game_phase import GamePhase
from app.exceptions.not_found import NotFoundError
from app.models.dto.game import GameInfo
from app.models.sql.bid import Bid
from app.models.sql.game import Game
from app.services.database.dragonfly.repository import DragonflyRepository
from app.services.database.postgres.repositories.general import Repository
from app.services.websockets import WebSocketManager
from app.utils.time import datetime_now


class GameController:
    repository: Repository
    dragonfly: DragonflyRepository
    ws_manager: WebSocketManager
    stollen_session: AiohttpSession

    def __init__(
        self,
        repository: Repository,
        dragonfly: DragonflyRepository,
        ws_manager: WebSocketManager,
        stollen_session: AiohttpSession,
    ):
        self.repository = repository
        self.dragonfly = dragonfly
        self.ws_manager = ws_manager
        self.stollen_session = stollen_session

    async def get_eth_rate(self) -> Decimal:
        session = await self.stollen_session.get_session()
        async with session.get(
            "https://api.binance.com/api/v3/ticker/price",
            params={"symbol": "ETHUSDC"},
        ) as response:
            data = await response.json()

            return Decimal(data["price"])

    async def get_last_game_info(self) -> GameInfo:
        game: Optional[Game] = await self.repository.games.get_last()
        if not game:
            raise NotFoundError("Game not found")

        return GameInfo(
            game_id=game.id,
            phase=game.phase,
            start_eth_price_usdc=game.start_eth_price_usdc,
            current_phase_start_time=game.current_phase_start_time,
            stats=await game.get_stats(),
            started_at=game.created_at,
            ended_at=game.ended_at if game.ended_at else None,
        )

    async def place_bid(self, signed_transaction: str) -> None:
        raise NotImplementedError

    async def remove_bid(self, wallet: str, bid_id: int) -> None:
        raise NotImplementedError

    async def get_user_bids(self, wallet: str) -> list[Bid]:
        raise NotImplementedError

    async def begin_game(self) -> GameInfo:
        game: Game = Game(
            start_eth_price_usdc=await self.get_eth_rate(),
            current_phase_start_time=datetime_now(),
        )
        await self.repository.uow.commit(game)
        return GameInfo(
            game_id=game.id,
            phase=game.phase,
            start_eth_price_usdc=game.start_eth_price_usdc,
            current_phase_start_time=game.current_phase_start_time,
            stats=await game.get_stats(),
            started_at=game.created_at,
            ended_at=None,
        )

    async def change_game_phase_to_waiting(self) -> GameInfo:
        game: Optional[Game] = await self.repository.games.get_last()
        if not game:
            raise NotFoundError("Game not found")

        game.phase = GamePhase.WAITING
        await self.repository.uow.commit(game)

        return GameInfo(
            game_id=game.id,
            phase=game.phase,
            start_eth_price_usdc=game.start_eth_price_usdc,
            current_phase_start_time=game.current_phase_start_time,
            stats=await game.get_stats(),
            started_at=game.created_at,
            ended_at=None,
        )
