import datetime

import jwt

from src.config import settings


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

