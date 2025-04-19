from uuid import UUID

from sqlalchemy import select, insert

from src.database.database import async_session_maker
from src.database.models import Message, Chat


class MessageRepository:

    @staticmethod
    async def find_message_by_chat_id(chat_id: UUID, user_id) -> list[dict]:
        async with async_session_maker() as session:
            query = (select(
                Message.id,
                Message.content,
                Message.is_human,
                Message.created_at)
                .join(Chat, Chat.id == Message.chat_id)
                     .where(Message.chat_id == chat_id, Chat.user_id == user_id))
            data = await session.execute(query)
            return data.mappings().all()

    @staticmethod
    async def create(**values) -> UUID:
        async with async_session_maker() as session:
            query = insert(Message).values(**values).returning(Message.id)
            id = await session.execute(query)
            await session.commit()
            return id.scalar()