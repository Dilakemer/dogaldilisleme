from typing import Optional, List
from .intent_patterns import INTENT_PATTERNS
from .intent_rules import detect_intent  # fonksiyon bazlı ise
from services.extractors import (extract_amount,extract_city,extract_customer_name,extract_date,extract_min_products,extract_product,extract_product_quantity)
class IntentClassifier:
    def __init__(self, products: Optional[List[str]] = None, debug: bool = False):
        self.products = products or []
        self.debug = debug
        self.intent_patterns = INTENT_PATTERNS

    def log(self, message: str):
        if self.debug:
            print(f"[DEBUG] {message}")

    def classify(self, text: str) -> str:
        # Öncelikle özel intent kurallarını deneyelim (fonksiyon bazlı)
        special_intent = detect_intent(text, products=self.products)
        if special_intent:
            self.log(f"Detected special intent: {special_intent}")
            return special_intent

        # Ardından regex patternlerle intent tespiti
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    self.log(f"Detected intent: {intent}")
                    return intent

        self.log("Detected intent: unknown")
        return "unknown"

    # Extractor fonksiyonlarını çağıran metodlar
    def extract_city(self, text: str) -> Optional[str]:
        return extract_city(text)

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
        return extract_amount(text)  # alias
    
    def extract_product(self, text: str) -> Optional[str]:
        return extract_product(text, self.products)
