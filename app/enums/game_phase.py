from enum import StrEnum, auto


class GamePhase(StrEnum):
    BIDDING = auto()
    SIGNING = auto()
    REVEALING = auto()
    FINISHED = auto()
    COMPLETED = (
        auto()
    )  # Used for the final state of the game, after game results are sent to the frontend.
