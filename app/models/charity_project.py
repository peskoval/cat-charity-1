from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import MAX_NAME_LENGTH

from app.models.base import InvestitionBase


class CharityProject(InvestitionBase):

    name: Mapped[str] = mapped_column(
        String(MAX_NAME_LENGTH),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        parts = [
            super().__repr__(),
            f'name={self.name}, '
            f'description={self.description}'
        ]
        return ', '.join(parts)
