# services/intents/intent_patterns.py
import re

INTENT_PATTERNS = {
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
    "customers_spending_min": [
        re.compile(
            r"toplamda\s*(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+)?)\s*tl\s*['‘’`\"]?\s*den\s*fazla harcama yapan",
            re.I,
        ),
        re.compile(
            r"(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+)?)\s*tl\s*['‘’`\"]?\s*den\s*fazla harcama yapan",
            re.I,
        ),
    ],
    "sales_on_date": [
        re.compile(r"\d{4}-\d{2}-\d{2}"),
        re.compile(r"tarihinde satış", re.I)
    ],
    "top_spenders_over_amount": [
        re.compile(
            r"(\d+(?:[\.,]\d+)?)\s*tl.*(üzerinde|den\s*fazla|’den\s*fazla|’dan\s*fazla).*harcama yapan müşteriler",
            re.I,
        ),
        re.compile(
            r"toplam.*harcama.*(\d+(?:[\.,]\d+)?)\s*tl.*geçen müşteriler",
            re.I,
        ),
    ],
    "customers_by_product": [
        re.compile(r"faturalarında\s*[\"']?(.+?)[\"']?\s*geçen", re.I),
        re.compile(r"faturasında.*\b(\w+)\b", re.I),
        re.compile(r"(.+) alan müşterilerin adres", re.I),
    ]

}
