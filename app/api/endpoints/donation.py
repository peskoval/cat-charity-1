from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
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
    donation_obj = await donation_crud.create(donation, session, commit=False)
    session.add_all(invest_donation(
        donation_obj,
        await charity_project_crud.get_active_objects(session),
    ))
    await session.commit()
    await session.refresh(donation_obj)
    return donation_obj


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
