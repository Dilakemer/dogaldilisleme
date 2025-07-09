from services.embedding_generator import EmbeddingGenerator
import json
class QuestionDatabase:
    def __init__(self, json_path="data/questions.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # JSON'daki key'ler sorular, value'lar cevaplar
        self.questions = list(data.keys())
        self.answers = list(data.values())

        self.embedder = EmbeddingGenerator()
        self.embedder.fit(self.questions)

    def find_most_similar(self, user_question):
        user_emb = self.embedder.embed(user_question)
        max_sim = -1
        best_idx = -1
        for idx, emb in enumerate(self.embedder.embeddings):
            sim = self.embedder.similarity(user_emb, emb)
            if sim > max_sim:
                max_sim = sim
                best_idx = idx
        if max_sim < 0.2:  # Çok düşük eşik, anlaşılamadı demek için
            return None, 0
        return self.answers[best_idx], max_sim

QUESTIONS_ANSWERS = QuestionDatabase()