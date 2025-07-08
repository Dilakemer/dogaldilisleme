import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class QuestionDatabase:
    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.qa_dict = json.load(f)
        self.questions = list(self.qa_dict.keys())
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.question_embeddings = self.model.encode(self.questions)

    def find_most_similar(self, user_question, threshold=0.7):
        user_emb = self.model.encode([user_question])
        similarities = cosine_similarity(user_emb, self.question_embeddings)[0]
        max_idx = np.argmax(similarities)
        max_sim = similarities[max_idx]
        if max_sim >= threshold:
            return self.questions[max_idx], self.qa_dict[self.questions[max_idx]]
        else:
            return None, None
