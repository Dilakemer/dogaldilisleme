from db.connection import run_query
from db.queries import get_all_product_names

def load_products_from_db():
    rows = run_query(get_all_product_names())
    # rows [(product_name1,), (product_name2,), ...]
    return [row[0].lower() for row in rows if row[0]]
