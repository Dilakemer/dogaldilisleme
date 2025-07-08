from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/TESTDB")

def run_query(query: str):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()
