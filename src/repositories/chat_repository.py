from uuid import UUID

from sqlalchemy import select, insert

from src.database.database import async_session_maker
from src.database.models import Chat
from src.schemas.chat_schema import ChatS


class ChatRepository:

    @staticmethod
    async def fide_chats_by_user_id(id: UUID) -> [dict]:
        async with async_session_maker() as session:
            query = select(Chat.name, Chat.created_at).where(Chat.user_id == id)
            data = await session.execute(query)
            return data.mappings().all()

    @staticmethod
    async def create(**values) -> UUID:
        async with async_session_maker() as session:
            query = insert(Chat).values(**values).returning(Chat.id)
            id = await session.execute(query)
            await session.commit()

            return id.scalar()