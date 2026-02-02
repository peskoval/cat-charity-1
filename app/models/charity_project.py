from typing import Optional
from datetime import datetime

from sqlalchemy import String, Integer, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import DEFAULT_INVESTED_AMOUNT, MAX_NAME_LENGTH
from app.core.db import Base, CommonMixin


class CharityProject(CommonMixin, Base):
    __tablename__ = 'charityproject'
    name: Mapped[str] = mapped_column(
        String(MAX_NAME_LENGTH),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=DEFAULT_INVESTED_AMOUNT,
        nullable=False,
    )
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
