from .intent_classifier import IntentClassifier
from db.query_builder import QueryBuilder
from handlers.address_query_handler import AddressQueryHandler
from handlers.customer_spending_handler import CustomerSpendingHandler
from handlers.total_sales_handler import TotalSalesHandler
from handlers.customers_spending_min_handler import CustomersSpendingMinHandler
from handlers.customers_min_product_handler import CustomersMinProductsHandler
from handlers.customers_by_product_handler import CustomersByProductHandler
from handlers.customers_have_one_invoice_line_handler import CustomersHaveOneInvoiceLineHandler
from handlers.most_expensive_product_invoice_handler import MostExpensiveProductInvoiceHandler
from handlers.top_spenders_recent_handler import TopSpendersRecentHandler

class ResponseGenerator:
    def __init__(self, products=None, debug=False):
        self.classifier = IntentClassifier(products=products, debug=debug)
        self.query_builder = QueryBuilder()

        self.intent_map = {
            "address_query": AddressQueryHandler(self.query_builder, self.classifier),
            "total_sales": TotalSalesHandler(self.query_builder, self.classifier),
            "customer_spending": CustomerSpendingHandler(self.query_builder, self.classifier),
            "customers_spending_min": CustomersSpendingMinHandler(self.query_builder, self.classifier),
            "customers_min_products": CustomersMinProductsHandler(self.query_builder, self.classifier),
            "customers_by_product": CustomersByProductHandler(self.query_builder, self.classifier),
            "customers_have_one_invoice_line": CustomersHaveOneInvoiceLineHandler(self.query_builder, self.classifier),
            "most_expensive_product_invoice": MostExpensiveProductInvoiceHandler(self.query_builder, self.classifier),
            "top_spenders_recent": TopSpendersRecentHandler(self.query_builder, self.classifier)
        }

        self.intent_titles = {
            "address_query": "📍 Adres Sorgusu",
            "total_sales": "💰 Toplam Satış Tutarı",
            "customer_spending": "🧾 Müşteri Harcaması",
            "customers_spending_min": "🛒 Belirli Tutar Üzerinde Harcama Yapan Müşteriler",
            "customers_min_products": "📦 En Az Belirli Sayıda Ürün Alan Müşteriler",
            "customers_by_product": "🔎 Ürün Bazlı Müşteri Sorgusu",
            "customers_have_one_invoice_line": "📃 Tek Fatura Satırı Olan Müşteriler",
            "most_expensive_product_invoice": "🏆 En Pahalı Ürün Kalemli Fatura",
            "top_spenders_recent": "📊 Son 30 Günün En Çok Harcayan Müşterileri"
        }

    def generate(self, user_input: str) -> str:
        intents = self.classifier.classify(user_input)
        responses = []

        for intent in intents:
            handler = self.intent_map.get(intent)
            if not handler:
                continue  # handler bulunamadıysa geç

            response = handler.handle(user_input)
            title = self.intent_titles.get(intent, intent.replace("_", " ").title())
            responses.append(f"**{title}**\n{response}\n")

        if responses:
            return "\n---\n".join(responses)

        return "Sorduğunuzu anlayamadım, lütfen tekrar deneyin."
