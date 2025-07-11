import re
import difflib
from typing import List, Optional, Tuple
from datetime import datetime
import nltk

def extract_min_products(text: str) -> int:
    match = re.search(r"en az\s*(\d+)", text, re.I)
    return int(match.group(1)) if match else 3

def extract_product(text: str, products: List[str]) -> Optional[str]:
    text_lower = text.lower().strip().replace('"', '').replace("'", "")
    for product in products:
        if product.lower() in text_lower:
            return product

    # Yakın eşleşme denemesi (örn. yazım hatası varsa)
    words = text_lower.split()
    for word in words:
        match = difflib.get_close_matches(word, products, n=1, cutoff=0.8)
        if match:
            return match[0]

    return None

def extract_customer_name(text: str) -> Optional[str]:
    matches = re.findall(r"\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+", text)
    return matches[0] if matches else None

def extract_amount(text: str) -> float:
    import re
    match = re.search(r"(\d+(?:[\.,]\d+)?)\s*(?:tl|₺)?", text, re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", "."))
    return 0.0


def extract_date(text: str) -> Optional[str]:
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    if match:
        try:
            datetime.strptime(match.group(), "%Y-%m-%d")
            return match.group()
        except ValueError:
            return None
    return None

def extract_product_quantity(text: str, products: List[str]) -> Tuple[Optional[str], int]:
    tokens = nltk.word_tokenize(text.lower())
    product_found = next((p for p in products if p.lower() in tokens), None)

    quantity_match = re.search(r"(\d+)\s*adet", text.lower())
    if quantity_match:
        return product_found, int(quantity_match.group(1))
    if re.search(r"kaç\s*adet", text.lower()):
        return product_found, -1
    return product_found, 0

def extract_city(text: str) -> Optional[str]:
    # Bilinen şehir isimlerinden regex ile kontrol
    cities = ["ankara", "istanbul", "izmir", "adana", "antalya"]
    for city in cities:
        if re.search(r"\b" + city + r"\b", text.lower()):
            return city.capitalize()
    return None
