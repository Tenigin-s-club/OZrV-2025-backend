from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SChat(BaseModel):
    id: UUID
    name: str
    created_at: datetime

class SAnswer(BaseModel):
    chat_id: UUID
    message: str

class SCreateChat(BaseModel):
    name: str
    user_id: UUID

