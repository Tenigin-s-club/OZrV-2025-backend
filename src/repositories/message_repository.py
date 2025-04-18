from uuid import UUID

from sqlalchemy import select

from src.database.database import async_session_maker
from src.database.models import Message


class MessageRepository:

    @staticmethod
    async def fide_message_by_chat_id(chat_id: UUID) -> list[dict]:
        async with async_session_maker() as session:
            query = select(Message.id, Message.content, Message.is_human, Message.created_at).where(Message.id == chat_id)
            data = session.execute(query)
            return data.meppings().all()