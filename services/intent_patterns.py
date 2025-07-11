# services/intents/intent_patterns.py
import re

INTENT_PATTERNS = {
    "customers_min_products": [
        re.compile(r"en az\s*(\d+)\s*farkli urun.*musteri", re.I),
        re.compile(r"kac farkli urun al", re.I),
        re.compile(r"birden fazla urun alan musteriler", re.I),
    ],

    "address_query": [
        re.compile(r"\b(izmir|ankara|adana|istanbul|antalya)(de|da|den|dan|li|lı|lu|lü)?\b", re.I)
    ],

    "total_sales": [
        re.compile(r"toplam satis", re.I),
        re.compile(r"ne kadar satis", re.I),
        re.compile(r"satis tutari", re.I)
    ],

    "customer_spending": [
        re.compile(r"(\b[a-zçğıöşü]+\s+[a-zçğıöşü]+)\s+ne kadar harcamış"),
        re.compile(r"(\b[a-zçğıöşü]+\s+[a-zçğıöşü]+)\s+harcaması"),
    ],

    "customers_spending_min": [
        re.compile(
            r"toplamda\s*(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+)?)\s*tl.*den fazla harcama yapan", re.I
        ),
        re.compile(
            r"(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+)?)\s*tl.*den fazla harcama yapan", re.I
        ),
    ],

    "sales_on_date": [
        re.compile(r"\d{4}-\d{2}-\d{2}"),
        re.compile(r"tarihinde satis", re.I)
    ],

    "top_spenders_over_amount": [
        re.compile(
            r"(\d+(?:[\.,]\d+)?)\s*tl.*(uzerinde|den fazla|dan fazla).*harcama yapan musteriler", re.I
        ),
        re.compile(
            r"toplam.*harcama.*(\d+(?:[\.,]\d+)?)\s*tl.*gecen musteriler", re.I
        ),
    ],

    "customers_by_product": [
        re.compile(r"faturalarinda\s*[\"']?(.+?)[\"']?\s*gecen", re.I),
        re.compile(r"faturasinda.*\b(\w+)\b", re.I),
        re.compile(r"(.+?) alan musterilerin adres", re.I),
    ],

    "customers_have_one_invoice_line": [
        re.compile(r"(icinde|içinde)?\s*sadece\s*tek\s*bir\s*fatura\s*satiri", re.I),
        re.compile(r"tek\s*bir\s*fatura\s*satiri\s*olan", re.I),
        re.compile(r"tek\s*fatura\s*satiri\s*(olan|iceren|bulunan)", re.I),
        re.compile(r"tek\s*bir\s*satir.*fatura", re.I),
    ],
    
    "most_expensive_product_invoice":[
         re.compile(
    r"(en\s+pahalı\s+ürün|en\s+yüksek\s+birim\s+fiyat(lı)?\s+ürün|en\s+pahalı\s+kalem).*(fatura\s+numarası|fatura\s+no|fatura)\s*(müşteri\s+adı|müşteri|isim|ad|ürün\s+adı|ürün)?", re.I)   ],
    
    "most_expensive_product_invoice": [
        re.compile(r"en\s*pahalı.*(birim\s*fiyat)?.*fatura.*", re.IGNORECASE),
        re.compile(r"birim\s*fiyatı\s*en\s*yüksek\s*ürün.*", re.IGNORECASE),
    ],

    "top_spenders_recent": [
    re.compile(r"son\s*(\d+)?\s*gün.*en\s*fazla.*(harcayan|tutar).*musteri", re.I),
    re.compile(r"en\s*fazla.*toplam.*fatura.*tutar.*musteri", re.I),
    re.compile(r"top\s*(\d+)?\s*musteri.*(en|fazla).*harcama", re.I),
]

}
