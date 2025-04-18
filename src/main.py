from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from src.bert import BertModel
from src.config import settings
from src.routers import routers_list

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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/question')
def ask_question(question: str = Body(embed=True)):
    model_facade = BertModel(settings.POSTGRES_URL, "")
    return model_facade.find_best(question)

for router in routers_list:
    app.include_router(router)