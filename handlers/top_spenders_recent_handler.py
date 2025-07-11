from handlers.base_handler import BaseHandler
from db.connection import run_query  

class TopSpendersRecentHandler(BaseHandler):
    def handle(self, user_input: str) -> str:
        query = self.query_builder.get_top_spenders_recent(limit=3)
        result = run_query(query)

        if not result:
            return "Son 30 gün içinde harcama yapan müşteri bulunamadı."

        rows = [f"- {row[0]}: {row[1]:.2f} ₺" for row in result]  # row[0]: name, row[1]: total_spent
        response = "Son 30 gün içinde en fazla toplam fatura tutarına ulaşan 3 müşteri:\n" + "\n".join(rows)
        return f"{response}\n\n[Oluşturulan SQL sorgusu]: {query}"
