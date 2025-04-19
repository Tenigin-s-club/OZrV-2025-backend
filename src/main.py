from contextlib import asynccontextmanager
from typing import Optional
from uuid import UUID, uuid4

import requests
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



def yandex_translate(text, api_key: str, target_lang='en'):
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {api_key}"
    }

    body = {
        "texts": [text],
        "targetLanguageCode": target_lang
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()['translations'][0]['text']
    else:
        return f"Ошибка: {response.text}"


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
    translated_text = yandex_translate("Егор я только что сделал переводчик большой член", "en")
    print(translated_text)
    try:
        user_id = await get_user_id(request)
    except Exception:
        return SAnswer(
            chat_id=UUID('00000000-0000-0000-0000-000000000000'),
            message=''.join(bert_model.find_best(question)),
            chat_message_id = uuid4(),
            human_message_id = uuid4()
        )

    if not chat_id:
        chat_id = await ChatRepository.create(**SCreateChat(name=question, user_id=user_id).model_dump())

    human_message_id = await MessageRepository.create(**SMessageCreate(is_human=True, content=question, chat_id=chat_id).model_dump())
    message = ''.join(bert_model.find_best(question))
    chat_message_id = await MessageRepository.create(**SMessageCreate(is_human=False, content=message, chat_id=chat_id).model_dump())

    return SAnswer(chat_id=chat_id, message=message, human_message_id=human_message_id, chat_message_id=chat_message_id)


@app.post('/question/{chat_id}')
async def ask_question_chat(request: Request, chat_id: UUID, question: str = Body(embed=True)) -> SAnswer:
    return await _process_question(request, question, chat_id)


@app.post('/question')
async def ask_question(request: Request, question: str = Body(embed=True)) -> SAnswer:
    return await _process_question(request, question)
for router in routers_list:
    app.include_router(router)
