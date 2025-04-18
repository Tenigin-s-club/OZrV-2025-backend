from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ChatS(BaseModel):
    id: UUID
    content: str
    human_is: bool
    created_at: datetime.datetime

