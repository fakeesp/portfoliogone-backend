from app.utils.key_builder import StorageKey


class LockGameBidsKey(StorageKey):
    game_id: int
