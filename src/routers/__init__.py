from fastapi import APIRouter

from .auth_router import router as auth_router
from .chat_router import router as chat_router
from .event_router import router as event_router

routers_list: list[APIRouter] = [auth_router, chat_router, event_router]

