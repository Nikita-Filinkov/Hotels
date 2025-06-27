from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker


class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_one_entry(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            await session.commit()
        return result.rowcount

    # @classmethod
    # async def update_one_entry(cls, model_id, **data):
    #     async with async_session_maker() as session:
    #         query = update(cls.model).filter_by(id=model_id).values(**data)
    #         result = await session.execute(query).returning(cls.model)
    #         await session.commit()
    #         return result.rowcount
