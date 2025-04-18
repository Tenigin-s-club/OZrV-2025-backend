import datetime
import uuid
from uuid import UUID
from sqlalchemy import exc

from fastapi import (APIRouter, HTTPException, Request, Response,
                     status)

from src.config import settings
from src.repositories.auth_repository import AuthRepository
from src.schemas.auth_schema import SLogin, SRegister, SUser
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


@router.delete('/delete_user/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID) -> None:
    await AuthRepository.delete(id)
