import re
from datetime import datetime
from typing import Optional, List, Tuple
import nltk

class IntentClassifier:
    def __init__(self, products: Optional[List[str]] = None, debug: bool = False):
        self.products = products or []
        self.debug = debug

        # Intent ve regex kalıplarını tutan dict
        self.intents = {
            "customers_min_products": [
                re.compile(r"en az\s*(\d+)\s*farklı ürün", re.I),
                re.compile(r"kaç farklı ürün aldı", re.I),
                re.compile(r"birden fazla ürün alan müşteriler", re.I),
            ],
            "customer_product_quantity": [
                re.compile(r"kaç\s*adet", re.I),
                re.compile(r"al[dıi](mış|mı|mi|mu|mü)?|satın\s*al[dıi](mış|mı|mi|mu|mü)?", re.I),
            ],
            "address_query": [
                re.compile(r"\b(izmir|ankara|adana|istanbul|antalya)(de|da|den|dan|li|lı|lu|lü)?\b", re.I)
            ],
            "total_sales": [
                re.compile(r"toplam satış|ne kadar satış|satış tutarı", re.I)
            ],
            "customer_spending": [
                re.compile(r"harcadı|ne kadar ödedi", re.I)
            ],
            "top_spenders": [
                re.compile(r"en çok harcayan|en fazla harcayan|en çok harcama yapan|en fazla harcama yapan", re.I)
            ],
            "sales_on_date": [
                re.compile(r"\d{4}-\d{2}-\d{2}"),
                re.compile(r"tarihinde satış", re.I)
            ],
        }

    def extract_min_products(self, text: str) -> int:
        match = re.search(r"en az\s*(\d+)", text, re.I)
        if match:
            return int(match.group(1))
        return 3

    def log(self, message: str):
        if self.debug:
            print(f"[DEBUG] {message}")

    def tokenize(self, text: str) -> List[str]:
        # nltk punkt tokenizer kullanılıyor, öncelikle nltk.download('punkt') yapılmalı
        tokens = nltk.word_tokenize(text.lower())
        self.log(f"Tokens: {tokens}")
        return tokens

    def classify(self, text: str) -> str:
        text_lower = text.lower()

        # Ürün var mı kontrolü
        if any(product in text_lower for product in self.products):
            if any(regex.search(text_lower) for regex in self.intents["customer_product_quantity"]):
                self.log("Detected intent: customer_product_quantity")
                return "customer_product_quantity"

        # Diğer intentleri sırayla kontrol et
        for intent, patterns in self.intents.items():
            if intent == "customer_product_quantity":  # yukarıda zaten kontrol ettik
                continue
            for pattern in patterns:
                if pattern.search(text):
                    self.log(f"Detected intent: {intent}")
                    return intent

        self.log("Detected intent: unknown")
        return "unknown"

    def extract_city(self, text: str) -> Optional[str]:
        match = re.search(r"\b(izmir|ankara|adana|istanbul|antalya)\b", text, re.I)
        if match:
            city = match.group(1).capitalize()
            self.log(f"Extracted city: {city}")
            return city
        return None

    def extract_customer_name(self, text: str) -> Optional[str]:
        matches = re.findall(r"\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+", text)
        if matches:
            self.log(f"Extracted customer name: {matches[0]}")
            return matches[0]
        return None

    def extract_date(self, text: str) -> Optional[str]:
        match = re.search(r"\d{4}-\d{2}-\d{2}", text)
        if match:
            try:
                datetime.strptime(match.group(), "%Y-%m-%d")
                self.log(f"Extracted date: {match.group()}")
                return match.group()
            except ValueError:
                return None
        return None

    def extract_product_quantity(self, text: str) -> Optional[Tuple[Optional[str], int]]:
        tokens = self.tokenize(text)
        product_found = None

        for product in self.products:
            if product.lower() in tokens:
                product_found = product
                break

        quantity_match = re.search(r"(\d+)\s*adet", text.lower())
        if quantity_match:
            quantity = int(quantity_match.group(1))
            self.log(f"Extracted quantity: {quantity} for product: {product_found}")
            return (product_found, quantity)

        if re.search(r"kaç\s*adet", text.lower()):
            self.log(f"Quantity is a question for product: {product_found}")
            return (product_found, -1)

        return (product_found, 0)  # Adet bilgisi yoksa 0 dönebiliriz
