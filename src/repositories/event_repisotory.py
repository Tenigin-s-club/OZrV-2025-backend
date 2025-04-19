from datetime import datetime
from uuid import UUID

from sqlalchemy import select, insert

from src.database.database import async_session_maker
from src.database.models import Event


class EventRepository:

    @staticmethod
    async def create(**values) -> UUID:
        async with async_session_maker() as session:
            query = insert(Event).values(**values).returning(Event.id)
            id = await session.execute(query)
            await session.commit()
            return id.scalar()

    @staticmethod
    async def find_full_event_by_id(id: UUID) -> dict:
        async with async_session_maker() as session:
            query = select(Event.__table__.columns).where(Event.id == id)
            data = await session.execute(query)
            return data.mappings().one_or_none()

    @staticmethod
    async def find_all() -> list[dict]:
        async with async_session_maker() as session:
            query = select(Event.__table__.columns).where(Event.date_event > datetime.now())
            data = await session.execute(query)
            return data.mappings().all()

    @staticmethod
    async def find_date_by_id(id: UUID) -> datetime:
        async with async_session_maker() as session:
            query = select(Event.date_event).where(Event.id == id)
            data = await session.execute(query)
            return data.scalar()