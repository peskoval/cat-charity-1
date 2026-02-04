from typing import Optional

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestitionBase


class Donation(InvestitionBase):
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        parts = [
            super().__repr__(),
            f'comment={self.comment}, '
        ]
        return ', '.join(parts)
