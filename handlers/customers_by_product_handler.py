from .base_handler import BaseHandler
from db.connection import run_query

class CustomersByProductHandler(BaseHandler):
    def handle(self, text: str) -> str:
        product = self.classifier.extract_product(text)
        if not product:
            return "Ürün adı algılanamadı."

        query = self.query_builder.get_customers_by_product(product)
        result = run_query(query)

        if not result:
            return f'"{product}" ürünü için fatura kaydı bulunamadı.'

        response = f'"{product}" geçen faturaları olan müşteriler:\n'
        for name, address in result:
            response += f"- {name} ({address})\n"

        response += f"\n[Oluşturulan SQL sorgusu]:\n{query}"
        return response
