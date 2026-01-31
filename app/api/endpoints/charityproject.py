from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_new_project_amount,
    check_project_exists,
    check_project_status,
)
from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investitions import invest_to_new_project

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
    project = await charity_project_crud.create(project, session)
    invested_project = await invest_to_new_project(project, session)
    return invested_project


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
    project = await charity_project_crud.update_project(
        project, project_in, session
    )
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
    project = await charity_project_crud.delete_project(project, session)
    return project
