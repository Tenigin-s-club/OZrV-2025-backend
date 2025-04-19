import datetime
import uuid
from uuid import UUID
from sqlalchemy import exc

from fastapi import (APIRouter, HTTPException, Request, Response,
                     status)

from src.config import settings
from src.repositories.auth_repository import AuthRepository
from src.repositories.chat_repository import ChatRepository
from src.repositories.message_repository import MessageRepository
from src.schemas.auth_schema import SLogin, SRegister, SUser
from src.schemas.chat_schema import SChat
from src.utils.security.password import check_password, encode_password
from src.utils.security.token import decode as decode_jwt
from src.utils.security.token import encode as encode_jwt

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.get('/me')
async def me(request: Request) -> SUser:
    refresh_token = request.cookies.get(settings.auth.cookie_refresh)
    try:
        pyload = await decode_jwt(refresh_token.encode())
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'token timeout')

    sub = pyload['sub']
    user = await AuthRepository.find_by_id_or_none(uuid.UUID(sub))
    return SUser(**user)


@router.get('/all')
async def get_all_users(request: Request) -> list[SUser]:
    refresh_token = request.cookies.get(settings.auth.cookie_refresh)
    try:
        pyload = await decode_jwt(refresh_token.encode())
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'token timeout')

    sub = pyload['sub']
    users = await AuthRepository.find_all(uuid.UUID(sub))
    return [SUser(**user) for user in users]


@router.get('/admin/user/{user_id}')
async def get_user_by_id(request: Request, user_id: UUID) -> SUser:
    refresh_token = request.cookies.get(settings.auth.cookie_refresh)
    try:
        await decode_jwt(refresh_token.encode())
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'token timeout')

    user = await AuthRepository.find_by_id_or_none(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'user not found')
    return SUser(**user)


@router.get('/admin/chats/{user_id}')
async def get_chats_by_user_id(request: Request, user_id: UUID) -> list[SChat]:
    refresh_token = request.cookies.get(settings.auth.cookie_refresh)
    try:
        await decode_jwt(refresh_token.encode())
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'token timeout')

    chats = await ChatRepository.find_chats_by_user_id(user_id)
    return [SChat(**chat) for chat in chats]


@router.get('/admin/chat/{chat_id}')
async def get_admin_chat_by_chat_id(request: Request, chat_id: UUID):
    refresh_token = request.cookies.get(settings.auth.cookie_refresh)
    try:
        pyload = await decode_jwt(refresh_token.encode())
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'token timeout')

    sub = pyload['sub']
    messages = await MessageRepository.find_message_by_chat_id(chat_id, uuid.UUID(sub))
    return messages


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(data: SRegister) -> None:
    data.password = encode_password(data.password)
    try:
        await AuthRepository.create(**data.model_dump())
    except exc.IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "email already exist")

@router.post('/login')
async def login(response: Response, data: SLogin) -> None:
    user_credential = await AuthRepository.find_by_email_or_none(data.email)
    if not user_credential or not check_password(data.password, user_credential.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'invalid password or email')

    payload = {
        'sub': str(user_credential.id),
    }

    access_token = await encode_jwt(settings.auth.type_token.access, payload)
    refresh_token = await encode_jwt(settings.auth.type_token.refresh, payload)

    now = datetime.datetime.now(datetime.UTC)
    response.set_cookie(
        settings.auth.cookie_access,
        access_token,
        expires=(now + settings.auth.access_exp),
        samesite='lax',
    )
    response.set_cookie(
        settings.auth.cookie_refresh,
        refresh_token,
        httponly=True,
        expires=(now + settings.auth.refresh_exp),
        samesite='lax',
    )


@router.post('/refresh')
async def refresh(request: Request, response: Response) -> None:
    refresh_token = request.cookies.get(settings.auth.cookie_refresh)
    try:
        pyload = await decode_jwt(refresh_token.encode())
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'token timeout')

    sub = pyload['sub']
    payload = {
        'sub': sub,
    }

    access_token = await encode_jwt(settings.auth.type_token.access, payload)
    refresh_token = await encode_jwt(settings.auth.type_token.refresh, payload)

    now = datetime.datetime.now(datetime.UTC)
    response.set_cookie(
        settings.auth.cookie_access,
        access_token,
        samesite='lax',
        expires=(now + settings.auth.access_exp))
    response.set_cookie(
        settings.auth.cookie_refresh,
        refresh_token,
        httponly=True,
        samesite='lax',
        expires=(now + settings.auth.refresh_exp))


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.delete_cookie(settings.auth.cookie_access)
    response.delete_cookie(settings.auth.cookie_refresh)
