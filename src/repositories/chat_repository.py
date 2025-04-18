from uuid import UUID

from sqlalchemy import select

from src.database.database import async_session_maker
from src.database.models import Chat

class ChatRepository:

    @staticmethod
    async def fide_chats_by_user_id(id: UUID) -> [dict]:
        async with async_session_maker() as session:
            query = select(Chat.name, Chat.created_at).where(Chat.user_id == id)
            data = await session.execute(query)
            return data.mappings().all()