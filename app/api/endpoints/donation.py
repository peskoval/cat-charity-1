from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investitions import invest_donation


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=DonationDB,
    description='Создать пожертвование.',
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
):
    donation = await donation_crud.create(donation, session)
    invested_donation = await invest_donation(donation, session)
    return invested_donation


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    description='Показать список всех пожертвований.',
)
async def get_all_donations(
    session: SessionDep
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations
