from typing import Optional

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import CharityDonationBase, CommonMixin


class Donation(CommonMixin, CharityDonationBase):
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f'Donation {self.id} {self.comment}'
