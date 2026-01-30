from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, Text, BOOLEAN, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import DEFAULT_INVESTED_AMOUNT
from app.core.db import Base, CommonMixin


class Donation(Base, CommonMixin):
    __tablename__ = 'donation'
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=DEFAULT_INVESTED_AMOUNT,
        nullable=False,
    )
    fully_invested: Mapped[bool] = mapped_column(
        BOOLEAN, default=False,
        nullable=False,
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
