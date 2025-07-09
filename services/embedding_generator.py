from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingGenerator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.embeddings = None

    def fit(self, documents):
        self.embeddings = self.vectorizer.fit_transform(documents)

    def embed(self, text):
        return self.vectorizer.transform([text])

    def similarity(self, emb1, emb2):
        return cosine_similarity(emb1, emb2)[0][0]
