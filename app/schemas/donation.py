from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveInt

from app.core.constants import DEFAULT_INVESTED_AMOUNT


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None)
    full_amount: PositiveInt

    model_config = ConfigDict(extra='forbid')


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: NonNegativeInt = DEFAULT_INVESTED_AMOUNT
    fully_invested: bool = False
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
