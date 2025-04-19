from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SCreateEvent(BaseModel):
    title: str
    description: str
    image_url: str
    date_event: datetime

class SEventShort(BaseModel):
    id: UUID
    title: str
    image_url: str

class SEvent(BaseModel):
    id: UUID
    title: str
    description: str
    image_url: str
    date_event: datetime

class SEventUserCreate(BaseModel):
    user_id: UUID
    event_id: UUID