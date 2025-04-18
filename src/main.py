from contextlib import asynccontextmanager
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from src.bert import BertModel
from src.config import settings
from src.routers import routers_list


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bert_model
    bert_model = BertModel(settings.POSTGRES_URL, "")
    yield
    del bert_model


bert_model = None
app = FastAPI(
    root_path="/api"
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


@app.post('/question')
def ask_question(question: str = Body(embed=True)) -> str:
    return ''.join(bert_model.find_best(question))

for router in routers_list:
    app.include_router(router)
