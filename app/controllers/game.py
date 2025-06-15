from decimal import Decimal
from typing import Optional

from stollen.session.aiohttp import AiohttpSession

from app.enums.bid_type import BidType
from app.enums.game_phase import GamePhase
from app.exceptions.bid_is_already_exists import BidIsAlreadyExistsError
from app.exceptions.bidding import BiddingEndedError
from app.exceptions.not_found import NotFoundError
from app.models.config.assets.main import Assets
from app.models.dto.game import GameInfo
from app.models.sql.bid import Bid
from app.models.sql.game import Game
from app.services.database.dragonfly.repository import DragonflyRepository
from app.services.database.postgres.repositories.general import Repository
from app.utils.time import datetime_now


class GameController:
    repository: Repository
    dragonfly: DragonflyRepository
    stollen_session: AiohttpSession
    assets: Assets

    def __init__(
        self,
        repository: Repository,
        dragonfly: DragonflyRepository,
        stollen_session: AiohttpSession,
        assets: Assets,
    ):
        self.repository = repository
        self.dragonfly = dragonfly
        self.stollen_session = stollen_session
        self.assets = assets

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
            current_eth_price_usdc=await self.get_eth_rate(),
            current_phase_start_time=game.current_phase_start_time,
            stats=await game.get_stats(),
            started_at=game.created_at,
            ended_at=game.ended_at if game.ended_at else None,
        )

    async def check_game_signed_transaction(
        self,
        signed_transaction: str,
        transaction: str,
        user_wallet: str,
    ) -> None:
        raise NotImplementedError

    async def place_bid(
        self,
        game_id: int,
        signed_transaction: str,
        transaction: str,
        user_wallet: str,
        bid_type: BidType,
        amount: Decimal,
    ) -> None:
        await self.check_game_signed_transaction(
            signed_transaction=signed_transaction,
            transaction=transaction,
            user_wallet=user_wallet,
        )
        async with self.dragonfly.lock_bids_by_game(game_id=game_id):
            game: Optional[Game] = await self.repository.games.get(game_id)
            if not game:
                raise NotFoundError("Game not found")

            if game.phase != GamePhase.BIDDING:
                raise BiddingEndedError("Game is not in bidding phase")

            bid: Optional[Bid] = await self.repository.bids.get_by_signed_transaction(
                signed_transaction=signed_transaction,
            )

            if bid:
                raise BidIsAlreadyExistsError("Bid with this signed transaction already exists")

            bid = Bid(
                user_wallet=user_wallet,
                game_id=game.id,
                bid_type=bid_type,
                transaction=transaction,
                amount=amount,
                signed_transaction=signed_transaction,
            )

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
            current_eth_price_usdc=game.start_eth_price_usdc,
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
            current_eth_price_usdc=await self.get_eth_rate(),
            stats=await game.get_stats(),
            started_at=game.created_at,
            ended_at=None,
        )

    async def change_game_phase_to_finished(self) -> GameInfo:
        game: Optional[Game] = await self.repository.games.get_last()
        if not game:
            raise NotFoundError("Game not found")

        game.phase = GamePhase.FINISHED
        game.ended_at = datetime_now()

        rate: Decimal = await self.get_eth_rate()

        await self.repository.uow.commit(game)

        # TODO: split rewards

        return GameInfo(
            game_id=game.id,
            phase=game.phase,
            start_eth_price_usdc=game.start_eth_price_usdc,
            current_phase_start_time=game.current_phase_start_time,
            current_eth_price_usdc=rate,
            stats=await game.get_stats(),
            started_at=game.created_at,
            ended_at=game.ended_at,
        )

    async def update_game(self) -> GameInfo:
        game: Optional[Game] = await self.repository.games.get_last()
        if not game:
            raise NotFoundError("Game not found")

        await self.repository.uow.commit(game)

        return GameInfo(
            game_id=game.id,
            phase=game.phase,
            start_eth_price_usdc=game.start_eth_price_usdc,
            current_phase_start_time=game.current_phase_start_time,
            current_eth_price_usdc=await self.get_eth_rate(),
            stats=await game.get_stats(),
            started_at=game.created_at,
            ended_at=game.ended_at,
        )
