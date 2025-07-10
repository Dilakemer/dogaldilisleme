from .base_handler import BaseHandler
from db.connection import run_query

class AddressQueryHandler(BaseHandler):
    def handle(self, text: str) -> str:
        city = self.classifier.extract_city(text)
        if not city:
            return "Şehir adı algılanamadı."
        
        query = self.query_builder.get_customers_by_city(city)
        rows = run_query(query)
        
        if not rows:
            return f"{city} şehrinde müşteri bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
        
        customers_list = "\n".join(f"- {r[0]} ({r[1]})" for r in rows)
        return f"{city} şehrindeki müşteriler:\n{customers_list}\n\n[Oluşturulan SQL sorgusu]:\n{query}"
