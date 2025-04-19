from sqlalchemy import insert

from src.database.database import async_session_maker
from src.database.models import EventUser


class EventUserRepository:

    @staticmethod
    async def create(**values):
        async with async_session_maker() as session:
            query = insert(EventUser).values(**values)
            await session.execute(query)
            await session.commit()