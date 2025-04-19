import asyncio
from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, status, Request
import datetime

from src.repositories.auth_repository import AuthRepository
from src.repositories.event_repisotory import EventRepository
from src.repositories.event_user_repository import EventUserRepository
from src.schemas.event_schema import SCreateEvent, SEvent, SEventUserCreate
from src.utils.notification.mail import Mail
from src.utils.security.token import get_user_id
from src import schedule

router = APIRouter(
    prefix="/event",
    tags=["Event"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_event(event: SCreateEvent):
    id = await EventRepository.create(**event.model_dump())
    return {"id": id}

@router.get("")
async def get_all_events():
    events = await EventRepository.find_all()
    return [SEvent(**event) for event in events]

@router.get("/{id}")
async def get_by_id(id: UUID) -> SEvent:
    event = await EventRepository.find_full_event_by_id(id)
    return SEvent(**event)

@router.post("/{id}/subscribe")
async def subscribe(request: Request, id: UUID) -> None:
    user_id = await get_user_id(request)
    event_date = await EventRepository.find_date_by_id(id)
    time_live = event_date - datetime.datetime.now()
    if time_live > timedelta(minutes=2):
        user_data = await AuthRepository.find_by_id_or_none(user_id)

        event_data = await EventRepository.find_full_event_by_id(id)

        await schedule.add_task(
            Mail.send_event,
            event_date - timedelta(minutes=2),
            event_data["title"],
            event_data["description"],
            event_data["date_event"],
            user_data["email"]
        )
    await EventUserRepository.create(**SEventUserCreate(user_id=user_id, event_id=id).model_dump())