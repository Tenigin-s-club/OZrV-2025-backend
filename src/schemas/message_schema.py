from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from starlette.convertors import UUIDConvertor


class MessageS(BaseModel):
    id: UUID
    content: str
    is_human: bool
    created_at: datetime

class SMessageCreate(BaseModel):
    is_human: bool
    content: str
    chat_id: UUID