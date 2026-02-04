from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_empty_project,
    check_name_duplicate,
    check_new_project_amount,
    check_project_exists,
    check_project_status
)
from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investitions import invest_donation

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=CharityProjectDB,
    description='Создать целевой проект.',
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: SessionDep,
):
    await check_name_duplicate(project.name, session)
    project_obj = await charity_project_crud.create(
        project,
        session,
        commit=False,
    )
    active_donations = await donation_crud.get_active_objects(session)
    invested_donations = invest_donation(
        project_obj,
        active_donations,
    )
    if invested_donations:
        session.add_all(invested_donations)
    await session.commit()
    await session.refresh(project_obj)
    return project_obj


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    description='Показать список всех целевых проектов.',
)
async def get_all_charity_projects(
    session: SessionDep
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    description=(
        'Редактировать целевой проект. '
        'Закрытый проект нельзя редактировать; нельзя установить требуемую '
        'сумму меньше уже вложенной.'
    ))
async def partially_update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: SessionDep,
):
    project = await check_project_exists(
        project_id, session
    )
    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session)
    if project_in.full_amount is not None:
        await check_new_project_amount(
            project_id, project_in.full_amount, session
        )
    await check_project_status(project_id, session)
    project = await charity_project_crud.update(
        project, project_in, session, commit=False
    )
    if project.invested_amount == project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()

    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    description=(
        'Удалить целевой проект. '
        'Нельзя удалить проект, в который уже были инвестированы средства.'
    ))
async def remove_project(
    project_id: int,
    session: SessionDep,
):
    project = await check_project_exists(project_id, session)
    await check_project_status(project_id, session)
    await check_empty_project(project_id, session)
    project = await charity_project_crud.remove(project, session, commit=False)
    await session.commit()
    return project
