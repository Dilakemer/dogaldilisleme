from .base_handler import BaseHandler
from db.connection import run_query
class TotalSalesHandler(BaseHandler):
    def handle(self, text: str) -> str:
        query = self.query_builder.get_total_sales()
        result = run_query(query)
        if result and result[0][0] is not None:
            return f"Toplam satış tutarı: {result[0][0]:,.2f} ₺\n\n[Oluşturulan SQL sorgusu]:\n{query}"
        return f"Toplam satış bilgisi bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
