# services/loaders/customers_name_loader.py
from db.connection import run_query
from db.query_builder import QueryBuilder

def load_customer_names_from_db():
    qb = QueryBuilder()
    query = qb.get_all_customer_names()
    rows = run_query(query)
    return [row[0].strip().lower() for row in rows if row[0]]
