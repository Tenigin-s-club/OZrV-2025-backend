from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ChatS(BaseModel):
    id: UUID
    name: str
    created_at: datetime

