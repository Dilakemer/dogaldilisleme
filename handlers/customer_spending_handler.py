from .base_handler import BaseHandler
from db.connection import run_query

class CustomerSpendingHandler(BaseHandler):
    def handle(self, text: str) -> str:
        customer_name = self.classifier.extract_customer_name(text)
        if not customer_name:
            return "Müşteri adı algılanamadı."
        query = self.query_builder.get_customer_total_spending(customer_name)
        result = run_query(query)
        if result and result[0][1] is not None:
            return f"{customer_name} toplamda {result[0][1]:,.2f} ₺ harcamış.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
        return f"{customer_name} adlı müşteri için harcama verisi bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
