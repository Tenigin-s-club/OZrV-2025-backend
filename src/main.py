from contextlib import asynccontextmanager

import time
from logging import getLogger
from uuid import UUID, uuid4

from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from src.bert import BertModel
from src.config import settings
from src.database.database import async_session_maker
from src.repositories.chat_repository import ChatRepository
from src.repositories.message_repository import MessageRepository
from src.routers import routers_list
from src.schemas.chat_schema import SCreateChat, SAnswer
from src.schemas.message_schema import MessageS, SMessageCreate
from src.schemas.statistics_schema import SStatistics
from src.utils.security.token import get_user_id
from src.utils.translate.translate import translate_text


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


@app.middleware("http")
async def get_statistics(request: Request, call_next):
    if request.url != 'http://127.0.0.1:8080/api/question':
        return await call_next(request)

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 100
    getLogger("uvicorn.error").info(f'Process time: {process_time} msecs')
    async with async_session_maker() as session:
        query = text(f'INSERT INTO statistics (request_time) VALUES ({process_time})')
        await session.execute(query)
        await session.commit()
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/question')
def ask_question(question: str = Body(embed=True)) -> str:
    return ''.join(bert_model.find_best(question))


@app.get('/statistics')
async def get_statistics() -> list[SStatistics]:
    async with async_session_maker() as session:
        # сделать все дни
        query = text("SELECT to_char(requested_at, 'YYYY-MM-DD') as date, count(*) as requests_count, avg(request_time) as requests_avg_time from statistics GROUP BY requested_at")
        result = await session.execute(query)
        return result.mappings().all()

async def _process_question(request: Request, question: str, lenguage: str, chat_id: UUID | None = None) -> SAnswer:
    try:
        user_id = await get_user_id(request)
    except Exception:
        if lenguage != 'ru':
            message = await translate_text(''.join(bert_model.find_best(await translate_text(question))), lenguage)
        else:
            message = ''.join(bert_model.find_best(question))
        return SAnswer(
            chat_id=UUID('00000000-0000-0000-0000-000000000000'),
            message=message,
            chat_message_id = uuid4(),
            human_message_id = uuid4()
        )

    if not chat_id:
        chat_id = await ChatRepository.create(**SCreateChat(name=question, user_id=user_id).model_dump())

    human_message_id = await MessageRepository.create(**SMessageCreate(is_human=True, content=question, chat_id=chat_id).model_dump())

    if lenguage != 'ru':
        message = await translate_text(''.join(bert_model.find_best(await translate_text(question))), lenguage)
    else:
        message = ''.join(bert_model.find_best(question))

    chat_message_id = await MessageRepository.create(**SMessageCreate(is_human=False, content=message, chat_id=chat_id).model_dump())

    return SAnswer(chat_id=chat_id, message=message, human_message_id=human_message_id, chat_message_id=chat_message_id)


@app.post('/question/{chat_id}')
async def ask_question_chat(request: Request, chat_id: UUID, language: str, question: str = Body(embed=True)) -> SAnswer:
    return await _process_question(request, question, language, chat_id)


@app.post('/question')
async def ask_question(request: Request, language: str, question: str = Body(embed=True)) -> SAnswer:
    return await _process_question(request, question, language)
for router in routers_list:
    app.include_router(router)
