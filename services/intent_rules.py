# services/intents/intent_rules.py
from typing import Optional
import re
from services.intent_patterns import INTENT_PATTERNS

def detect_intent(text: str, products: list[str] = []) -> Optional[str]:
    text_lower = text.lower()

    # 1) "son fatura" + herhangi bir TL miktarı → kesin spending_min
    if "son fatura" in text_lower and re.search(r"\d+[\.,]?\d*\s*tl", text_lower):
        return "customers_spending_min"

    # 2) "TL den fazla harcama yapan" (genel harcama sorusu)
    if re.search(r"\d+[\.,]?\d*\s*tl", text_lower) and "harcama" in text_lower:
        return "customers_spending_min"

    # 3) faturalarında ürün geçen sorgular
    if "faturalarında" in text_lower:
        return "customers_by_product"

    # 4) ürün adı + kaç adet gibi sayısal soru
    if any(p in text_lower for p in products):
        for pattern in INTENT_PATTERNS.get("customer_product_quantity", []):
            if pattern.search(text_lower):
                return "customer_product_quantity"

    # 5) Diğer tüm intent’leri pattern’lerle IntentClassifier yapacak
    return None
