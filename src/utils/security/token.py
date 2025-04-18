import datetime
import uuid

import jwt
from starlette import status

from src.config import settings
from fastapi import Request, HTTPException


async def encode(
    type_token: str,
    payload: dict,
    key = settings.auth.private_key.read_text(),
    algorithm = settings.auth.algorithm,
):
    now = datetime.datetime.utcnow()
    
    if type_token == settings.auth.type_token.access:
        payload.update(
            iat = now,
            exp = now + settings.auth.access_exp
        )
    if type_token == settings.auth.type_token.refresh:
        payload.update(
            iat = now,
            exp = now + settings.auth.refresh_exp
        )
        
    return jwt.encode(payload, key, algorithm)

async def decode(
    token: str | bytes,
    key = settings.auth.public_key.read_text(),
    algorithm = settings.auth.algorithm
):      
    return jwt.decode(token, key, algorithm)

async def get_user_id(request: Request) -> uuid.UUID:
    refresh_token = request.cookies.get(settings.auth.cookie_refresh)
    try:
        pyload = await decode(refresh_token.encode())
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'token timeout')

    sub = pyload['sub']

    return uuid.UUID(sub)