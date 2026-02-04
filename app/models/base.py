from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, CheckConstraint, and_, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import CommonBase


class InvestitionBase(CommonBase):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            'full_amount > 0', name='check_full_amount_positive'
        ),
        CheckConstraint(
            and_(
                text('invested_amount >= 0'),
                text('invested_amount <= full_amount')
            ),
        ),
    )
    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    def __repr__(self):
        return (
            f'{super().__repr__()}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date})'
        )
