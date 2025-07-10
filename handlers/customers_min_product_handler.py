from .base_handler import BaseHandler
from db.connection import run_query

class CustomersMinProductsHandler(BaseHandler):
    def handle(self, text: str) -> str:
        min_products = self.classifier.extract_min_products(text)
        query = self.query_builder.get_customers_with_minimum_products(min_products)
        result = run_query(query)
        if result:
            response_list = "\n".join([f"- {row[0]}: {row[1]} farklı ürün" for row in result])
            return f"En az {min_products} farklı ürün satın alan müşteriler:\n{response_list}\n\n[Oluşturulan SQL sorgusu]:\n{query}"
        return f"Hiçbir müşteri en az {min_products} farklı ürün satın almamış.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
