from fastapi import FastAPI, Body

from src.bert import BertModel
from src.config import settings
from src.routers import routers_list

app = FastAPI()

@app.post('/question')
def ask_question(question: str = Body(embed=True)):
    model_facade = BertModel(settings.POSTGRES_URL, "")
    return model_facade.find_best(question)

for router in routers_list:
    app.include_router(router)