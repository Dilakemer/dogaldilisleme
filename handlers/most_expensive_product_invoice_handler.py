from .base_handler import BaseHandler
from db.connection import run_query
"""En pahalı ürün kalemini (birim fiyat olarak) içeren fatura numarası, müşteri adı ve ürün adını getir."""

class MostExpensiveProductInvoiceHandler(BaseHandler):
    def handle(self, user_input: str) -> str:
        query = self.query_builder.get_most_expensive_product_invoice()
        result = run_query(query)
        if result:
            row = result[0]
            return (f"En pahalı ürünün olduğu fatura:\n"
                    f"- Fatura No: {row[0]}\n"
                    f"- Müşteri: {row[1]}\n"
                    f"- Ürün: {row[2]}\n"
                    f"[Oluşturulan SQL sorgusu]: {query}")
        return "Herhangi bir sonuç bulunamadı."
