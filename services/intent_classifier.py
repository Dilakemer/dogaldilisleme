# services/intent_classifier.py

from typing import Optional, List
from .intent_patterns import INTENT_PATTERNS
from .intent_rules import detect_intent  # fonksiyon bazlı ise
from services.extractors import (
    extract_amount,
    extract_customer_name,
    extract_date,
    extract_min_products,
    extract_product,
    extract_product_quantity,
    extract_city
)
import unicodedata

from services.embedding_intent_classifier import EmbeddingIntentClassifier

class IntentClassifier:
    def __init__(self, products: Optional[List[str]] = None, debug: bool = False, use_embedding_classifier: bool = True):
        self.products = products or []
        self.debug = debug
        self.intent_patterns = INTENT_PATTERNS
        self.use_embedding_classifier = use_embedding_classifier

        if use_embedding_classifier:
            self.embedding_classifier = EmbeddingIntentClassifier(debug=debug)
            self.embedding_classifier.load("models/embedding_intent_classifier.pkl")

    def log(self, message: str):
        if self.debug:
            print(f"[DEBUG] {message}")

    def normalize_text(self, text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text)
        cleaned = ''.join(c for c in normalized if not unicodedata.combining(c))
        return cleaned.lower()

    # Değişen kısım: classify artık liste döndürüyor ve çoklu intent destekliyor
    def classify(self, text: str) -> List[str]:
        normalized_text = self.normalize_text(text)
        self.log(f"Classifying normalized text: {normalized_text}")

        detected_intents = set()

        # Kural tabanlı intent tespiti (rule-based)
        special_intent = detect_intent(normalized_text, products=self.products)
        self.log(f"detect_intent returned: {special_intent}")
        if special_intent:
            self.log(f"Detected special intent: {special_intent}")
            detected_intents.add(special_intent)

        # Regex pattern eşleşmeleri
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern.search(normalized_text):
                    self.log(f"Pattern matched intent: {intent} with pattern: {pattern.pattern}")
                    detected_intents.add(intent)

        # Bu satır embedding'i sadece önceki yollar başarısızsa çalıştırır
        if self.use_embedding_classifier and not detected_intents:
            intent = self.embedding_classifier.classify(text)
            self.log(f"Embedding classifier returned: {intent}")
            if intent != "unknown":
                detected_intents.add(intent)



        # Eğer hiç intent bulunamadıysa "unknown" döndür
        if not detected_intents:
            return ["unknown"]

        return list(detected_intents)

    # Extractor metodları (değişmedi)
    def extract_product(self, text: str) -> Optional[str]:
        return extract_product(text, self.products)

    def extract_customer_name(self, text: str) -> Optional[str]:
        return extract_customer_name(text)

    def extract_amount(self, text: str) -> float:
        return extract_amount(text)

    def extract_date(self, text: str) -> Optional[str]:
        return extract_date(text)

    def extract_product_quantity(self, text: str):
        return extract_product_quantity(text, self.products)

    def extract_min_products(self, text: str) -> int:
        return extract_min_products(text)

    def extract_min_spending(self, text: str) -> float:
        return extract_amount(text)

    def extract_location(self, text: str) -> Optional[str]:
        return extract_city(text)
    
    
