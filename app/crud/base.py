from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        commit: bool = True,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(
            **obj_in_data,
            invested_amount=0,
            fully_invested=False,
        )
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        db_obj = await session.get(self.model, obj_id)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
        commit: bool = True,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
        commit: bool = True,
    ):
        await session.delete(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def get_active_objects(
        self,
        session: AsyncSession
    ):
        active_objects = await session.execute(
            select(self.model)
            .where(
                self.model.close_date.is_(None),
                self.model.fully_invested.is_(False),
            )
            .order_by(asc(self.model.create_date))
        )
        return active_objects.scalars().all()
