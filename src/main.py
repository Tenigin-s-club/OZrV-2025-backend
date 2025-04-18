from fastapi import FastAPI, Body

from src.bert import BertModel
from src.config import settings

app = FastAPI()

@app.post('/question')
def ask_question(question: str = Body(embed=True)):
    model_facade = BertModel(settings.POSTGRES_URL, "")
    return model_facade.find_best(question)
