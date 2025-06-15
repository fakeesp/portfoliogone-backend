from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from app.models.sql.base import Base
from app.models.sql.mixins.timestamp import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    wallet: Mapped[str] = mapped_column(primary_key=True, unique=True, nullable=False)
