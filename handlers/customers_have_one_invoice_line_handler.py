from handlers.base_handler import BaseHandler
from db.connection import run_query  

class CustomersHaveOneInvoiceLineHandler(BaseHandler):
    def handle(self, user_input: str) -> str:
        sql_query = self.query_builder.get_customers_have_one_invoice_line()
        result = run_query(sql_query)  # self.run_query değil
        return self.format_result(result)

    def format_result(self, rows):
        if not rows:
            return "Tek fatura satırı olan müşteri bulunamadı."

        return "\n".join([
            f"{row[0]} - Fatura ID: {row[1]}" for row in rows
        ])
