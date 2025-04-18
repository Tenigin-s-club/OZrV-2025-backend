from numpy import array, float32
from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from logging import getLogger


class BertModel:
    def __init__(self, db_uri: str, llm_api_key: str):
        getLogger().error("Started initialization Bert model")
        self.model = SentenceTransformer('cointegrated/rubert-tiny2')
        self.session_factory = sessionmaker(create_engine(db_uri.replace('asyncpg', 'psycopg')))
        self._llm_api_key = llm_api_key
        getLogger().error("Ended initialization Bert model")

    def generate_embeddings(self, sentences: list[str]) -> list[float]:
        embs = self.model.encode(sentences)[0]
        return embs.tolist()

    def find_best(self, sentence: str) -> tuple[str, list[str]]:
        emb = self.generate_embeddings([sentence])

        with self.session_factory() as session:
            rows = session.execute(text(
                "SELECT question, answer, embedding, url FROM question_answers"
            )).all()

        distances = {}
        for i, item in enumerate(rows):
            question, answer, embedding, url = item
            embedding = array([float(elem) for elem in embedding[1:-1].split(',')], dtype=float32)
            getLogger().error(f'{emb}\n{embedding}\n{len(emb)}\n{len(embedding)}')
            dist = distance.cosine(emb, embedding)
            distances[(question, i)] = (dist, answer, url)

        dists = sorted(list(distances.items()), key=lambda a: a[1][0])[:10]

        closest_one = dists[0]

        # if closest_one[1][0] > 0.1:
        #     return 'Не получилось найти ответ - свяжитесь со специалистом техподдержки', []

        answer_links = set()
        best_answers = [closest_one[1][1]]

        occured_questions = {closest_one[0][0]}
        for question, answer in dists:
            question_text, _ = question
            dist, answer_text, url = answer

            if dist - closest_one[1][0] == 0:
                answer_links.add(url)
            elif dist - closest_one[1][0] < 0.04:
                if question_text not in occured_questions:
                    best_answers.append(answer_text)
                    occured_questions.add(question_text)

        print(f'{sentence}\n{best_answers}\n\nDistances: {dists}')
        return best_answers, answer_links
