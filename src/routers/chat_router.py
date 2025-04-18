import uuid
from uuid import UUID

from fastapi import APIRouter, Request, HTTPException
from starlette import status

from src.config import settings
from src.repositories.chat_repository import ChatRepository
from src.repositories.message_repository import MessageRepository
from src.schemas.chat_schema import ChatS
from src.utils.security.token import decode as decode_jwt
from src.utils.security.token import get_user_id

router = APIRouter(
    prefix="/chat",
    tags = ["Chat"]
)

@router.get("")
async def get_chat(request: Request):
    user_id = await get_user_id(request)
    chats = ChatRepository.fide_chats_by_user_id(user_id)
    return [ChatS(**chat) for chat in chats]

@router.get("/id")
async def get_messages(request: Request):
    user_id = await get_user_id(request)
    messages = MessageRepository.fide_message_by_chat_id(user_id)
    return