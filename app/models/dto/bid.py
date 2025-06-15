from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.enums.bid_type import BidType


class BidDto(BaseModel):
    id: int = Field(description="Unique identifier of the bid")
    user_wallet: str = Field(description="Wallet address of the user who placed the bid")
    game_id: int = Field(description="Unique identifier of the game associated with the bid")
    bid_type: BidType = Field(description="Type of the bid (LONG, SHORT, ZERO)")
    amount: Decimal = Field(description="Amount of USDC placed in the bid")
    has_transaction: bool = Field(
        description="Indicates whether the bid has an associated transaction"
    )
    created_at: datetime
