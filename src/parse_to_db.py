import json

from sqlalchemy import text
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.bert import BertModel
from logging import getLogger


def parse_to_db(uri: str):
    def create_db_engine(db_uri: str) -> Engine:
        engine_options = {
            "echo": False,
            "pool_size": 15,
            "max_overflow": 15,
        }
        return create_engine(db_uri, **engine_options)

    def create_session_maker(engine: Engine) -> sessionmaker[Session]:
        return sessionmaker(engine, autoflush=True, expire_on_commit=False)

    engine = create_db_engine(uri)
    session_factory = create_session_maker(engine)

    model_facade = BertModel(uri, "")

    with open(
        "./src/huesos.json",
        'r', encoding='utf-8'
    ) as f:
        data = json.load(f)
        with session_factory() as session:
            for row in data:
                emb = model_facade.generate_embeddings(row['question'])
                session.execute(
                    statement=text(
                        'INSERT INTO question_answers (question, answer, embedding, url) VALUES (:question, :answer, :embedding, :url)'),
                    params={
                        'question': row['question'],
                        'answer': row['answer'],
                        'url': row['url'],
                        'embedding': emb
                    },
                )
            session.commit()
