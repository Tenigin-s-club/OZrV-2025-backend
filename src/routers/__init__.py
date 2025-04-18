from fastapi import APIRouter

from .auth_router import router as auth_router

routers_list: list[APIRouter] = [auth_router]

