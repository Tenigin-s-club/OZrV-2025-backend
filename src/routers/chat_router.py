from uuid import UUID

from fastapi import APIRouter, Request

from src.repositories.chat_repository import ChatRepository
from src.repositories.message_repository import MessageRepository
from src.schemas.chat_schema import ChatS
from src.schemas.message_schema import MessageS
from src.utils.security.token import get_user_id

router = APIRouter(
    prefix="/chat",
    tags = ["Chat"]
)

@router.get("")
async def get_chat(request: Request):
    user_id = await get_user_id(request)
    chats = await ChatRepository.fide_chats_by_user_id(user_id)
    return [ChatS(**chat) for chat in chats]

@router.get("/chat_id")
async def get_messages(request: Request, chat_id: UUID):
    user_id = await get_user_id(request)
    messages = await MessageRepository.fide_message_by_chat_id(chat_id, user_id)
    return [MessageS(**message) for message in messages]