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

class QuestionDatabase:
    def __init__(self):
        # Buraya sorularını ve cevaplarını ekle
        self.questions = [
            "Ayşe Demir kaç adet hoparlör aldı?",
            "Ali Veli toplamda kaç yazıcı satın aldı?",
            "Toplam satış tutarı nedir?",
            # diğer sorular...
        ]
        self.answers = [
            "Ayşe Demir toplamda 5 hoparlör aldı.",
            "Ali Veli toplamda 3 yazıcı satın aldı.",
            "Toplam satış tutarı 1,000,000 ₺",
            # diğer cevaplar...
        ]

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
        if max_sim < 0.2:  # Eşik, çok düşükse "anlayamadım" dönebiliriz
            return None, 0
        return self.answers[best_idx], max_sim

# Test
if __name__ == "__main__":
    qdb = QuestionDatabase()
    user_input = "Ayşe Demir kaç yazıcı aldı?"
    answer, score = qdb.find_most_similar(user_input)
    if answer:
        print(f"Benzer cevap: {answer} (Benzerlik: {score:.2f})")
    else:
        print("Sorunuz anlaşılamadı, lütfen tekrar deneyin.")
