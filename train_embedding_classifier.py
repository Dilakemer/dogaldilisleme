# train_embedding_classifier.py

import pandas as pd
from services.embedding_intent_classifier import EmbeddingIntentClassifier
import pickle
import os

def main():
    # Klasör kontrolü
    os.makedirs("models", exist_ok=True)

    # Eğitim verisini oku
    df = pd.read_csv("data/training_data.csv")

    texts = df['text'].tolist()
    labels = df['label'].tolist()

    # Modeli oluştur ve eğit
    classifier = EmbeddingIntentClassifier(debug=True)
    classifier.train(texts, labels)

    # Modeli diske kaydet
    with open("models/embedding_intent_classifier.pkl", "wb") as f:
        pickle.dump({
            "vectorizer": classifier.vectorizer,
            "model": classifier.model
        }, f)
    print("Model eğitim ve kaydetme tamamlandı.")

if __name__ == "__main__":
    main()
