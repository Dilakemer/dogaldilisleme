# services/city_loader.py

from db.connection import run_query
from typing import List

def load_cities_from_db() -> List[str]:
    """
    Veritabanındaki customers tablosundan
    adres sütunundaki şehir kısımlarını çeker
    ve benzersiz, küçük harfli bir liste olarak döner.
    """
    # PostgreSQL SPLIT_PART ile virgülden önceki kısmı alıyoruz
    sql = """
        SELECT DISTINCT
          TRIM(SPLIT_PART(address, ',', 1)) AS city
        FROM customers
        WHERE address IS NOT NULL;
    """
    rows = run_query(sql)
    # rows: [(city1,), (city2,), ...]
    return [r[0].lower() for r in rows if r[0]]
