from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charityproject import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        charity_project: str,
        session: AsyncSession
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project
            )
        )
        return charity_project_id.scalars().first()

    async def get_project_by_id(
        self,
        project_id: int,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        project = await session.get(CharityProject, project_id)
        return project

    async def update_project(
        self,
        db_project: CharityProject,
        project_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_project)
        update_data = project_in.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        for field in obj_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def delete_project(
        self,
        project: CharityProject,
        session: AsyncSession
    ) -> CharityProject:
        await session.delete(project)
        await session.commit()
        return project


charity_project_crud = CRUDCharityProject(CharityProject)
