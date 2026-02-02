from typing import Annotated
from fastapi import HTTPException, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    DEFAULT_INVESTED_AMOUNT,
    NOT_UNIQUE_NAME,
    PROJECT_HAS_INVESTMENTS,
    PROJECT_NOT_FOUND,
    WRONG_AMOUNT,
    WRONG_PROJECT_STATUS,
)
from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.models.charity_project import CharityProject

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session,
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NOT_UNIQUE_NAME,
        )


async def check_new_project_amount(
    project_id: int,
    new_full_amount: int,
    session: SessionDep
):
    project = await charity_project_crud.get_project_by_id(project_id, session)
    if project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=WRONG_AMOUNT,
        )


async def check_project_status(
    project_id: int,
    session: SessionDep
):
    project = await charity_project_crud.get_project_by_id(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=WRONG_PROJECT_STATUS,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get_project_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    return project


async def check_empty_project(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get_project_by_id(project_id, session)
    if project.invested_amount > DEFAULT_INVESTED_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_HAS_INVESTMENTS
        )
