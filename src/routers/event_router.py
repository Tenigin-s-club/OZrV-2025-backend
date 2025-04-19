from uuid import UUID

from fastapi import APIRouter, status, Request

from src.repositories.event_repisotory import EventRepository
from src.repositories.event_user_repository import EventUserRepository
from src.schemas.event_schema import SCreateEvent, SEventShort, SEvent, SEventUserCreate
from src.utils.security.token import get_user_id

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
    return [SEventShort(**event) for event in events]

@router.get("/{id}")
async def get_by_id(id: UUID) -> SEvent:
    event = await EventRepository.find_full_event_by_id(id)
    return SEvent(**event)

@router.post("/{id}/subscribe")
async def subscribe(request: Request, id: UUID) -> None:
    user_id = await get_user_id(request)
    await EventUserRepository.create(**SEventUserCreate(user_id=user_id, event_id=id).model_dump())