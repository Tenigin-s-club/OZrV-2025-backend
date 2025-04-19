from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.database.database import async_session_maker
from src.database.models import User


class AuthRepository:
    @staticmethod
    async def find_by_id_or_none(id: UUID) -> dict | None:
        async with async_session_maker() as session:
            query = select(User.id, User.email, User.fio).where(User.id == id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @staticmethod
    async def find_by_email_or_none(email: str) -> dict:
        async with async_session_maker() as session:
            query = select(User.id, User.password).where(User.email == email)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @staticmethod
    async def find_all(id: UUID) -> list[dict]:
        async with async_session_maker() as session:
            query = select(User.__table__.columns).where(User.id != id)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def create(**values) -> None:
        async with async_session_maker() as session:
            query = insert(User).values(**values)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def delete(id: UUID) -> None:
        async with async_session_maker() as session:
            query = delete(User).where(User.id == id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def all_users_email() -> list[str]:
        async with async_session_maker() as session:
            query = select(User.email)
            data = await session.execute(query)

            return data.scalars().all()
