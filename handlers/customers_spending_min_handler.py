from .base_handler import BaseHandler
from db.connection import run_query

class CustomersSpendingMinHandler(BaseHandler):
    def handle(self, text: str) -> str:
        amount = self.classifier.extract_min_spending(text)
        query = self.query_builder.get_customers_spending_min(amount)
        rows = run_query(query)
        if rows:
            response = "\n".join(
                f"- {r[0]}: Son fatura {r[1]}, Toplam harcama {r[2]:,.2f} ₺"
                for r in rows
            )
        else:
            response = f"Toplamda {amount} ₺’den fazla harcama yapan müşteri bulunamadı."
        return (
            f"Toplamda {amount} ₺’den fazla harcama yapan müşteriler:\n"
            f"{response}\n\n[Oluşturulan SQL sorgusu]:\n{query}"
        )
