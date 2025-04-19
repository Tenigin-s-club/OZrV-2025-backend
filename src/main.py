from contextlib import asynccontextmanager
from typing import Optional
from uuid import UUID

from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware

from src.bert import BertModel
from src.config import settings
from src.repositories.chat_repository import ChatRepository
from src.repositories.message_repository import MessageRepository
from src.routers import routers_list
from src.schemas.chat_schema import SCreateChat, SAnswer
from src.schemas.message_schema import MessageS, SMessageCreate
from src.utils.security.token import get_user_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bert_model
    bert_model = BertModel(settings.POSTGRES_URL, "")
    yield
    del bert_model


bert_model = None
app = FastAPI(
    root_path="/api",
    lifespan=lifespan
)

origins = [
    'http://194.87.248.63:3000',
    'https://194.87.248.63:3000',
    'http://localhost:3000',
    'https://tunom.ru',
    'http://tunom.ru'
    'https://localhost:3000',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


async def _process_question(request: Request, question: str, chat_id: UUID | None = None) -> SAnswer:
    user_id = await get_user_id(request)

    if not chat_id:
        chat_id = await ChatRepository.create(**SCreateChat(name=question, user_id=user_id).model_dump())

    await MessageRepository.create(**SMessageCreate(is_human=True, content=question, chat_id=chat_id).model_dump())
    message = ''.join(bert_model.find_best(question))
    await MessageRepository.create(**SMessageCreate(is_human=False, content=message, chat_id=chat_id).model_dump())

    return SAnswer(chat_id=chat_id, message=message)


@app.post('/question/{chat_id}')
async def ask_question_chat(request: Request, chat_id: UUID, question: str = Body(embed=True)) -> SAnswer:
    return await _process_question(request, question, chat_id)


@app.post('/question')
async def ask_question(request: Request, question: str = Body(embed=True)) -> SAnswer:
    return await _process_question(request, question)
for router in routers_list:
    app.include_router(router)
