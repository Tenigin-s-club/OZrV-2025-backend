from datetime import datetime

from numpy import array, float32
from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from logging import getLogger


class BertModel:
    def __init__(self, db_uri: str, llm_api_key: str) -> None:
        getLogger().error("Started initialization Bert model")
        self.model = SentenceTransformer('cointegrated/rubert-tiny2')
        self.session_factory = sessionmaker(create_engine(db_uri.replace('asyncpg', 'psycopg')))
        self._llm_api_key = llm_api_key
        getLogger().error("Ended initialization Bert model")

    def generate_embeddings(self, sentence: str) -> list[float]:
        return self.model.encode(sentence).tolist()

    def find_best(self, sentence: str) -> tuple[str, str]:
        request_embs = self.generate_embeddings(sentence)

        with self.session_factory() as session:
            dataset_embs = session.execute(text(
                "SELECT question, answer, embedding, url FROM question_answers"
            )).all()

        distances = {}
        for i, item in enumerate(dataset_embs):
            question, answer, curr_emb, url = item
            curr_emb = list(map(float, curr_emb[1:-1].split(',')))
            curr_dist = distance.cosine(request_embs, curr_emb)
            distances[question] = (curr_dist, answer, url)

        best_distances = sorted(list(distances.items()), key=lambda a: a[1][0])[:3]
        closest_one_distance = best_distances[0]
        getLogger().error(f'{best_distances=}')

        if closest_one_distance[1][0] > 0.15:
            return 'Не получилось найти ответ, попробуйте перефразировать запрос или написать его целиком в одно предложение, пожалуйста', ''
        return closest_one_distance[1][1], closest_one_distance[1][2]
