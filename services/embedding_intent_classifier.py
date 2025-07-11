# services/embedding_intent_classifier.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class EmbeddingIntentClassifier:
    def __init__(self, debug=False):
        self.debug = debug
        self.vectorizer = None
        self.model = None
        self.is_trained = False

    def train(self, texts, labels):
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(texts)
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, labels)
        self.is_trained = True
        if self.debug:
            print("[DEBUG] Model eğitildi.")

    def load(self, path):
        import pickle
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.vectorizer = data["vectorizer"]
            self.model = data["model"]
            self.is_trained = True
        if self.debug:
            print(f"[DEBUG] Model yüklendi: {path}")

    def classify(self, text):
        if not self.is_trained:
            if self.debug:
                print("[DEBUG] Model yüklü değil!")
            return "unknown"
        x = self.vectorizer.transform([text])
        pred = self.model.predict(x)[0]
        if self.debug:
            print(f"[DEBUG] EmbeddingIntentClassifier prediction: {pred}")
        return pred
