from .intent_classifier import IntentClassifier
from db.query_builder import QueryBuilder
from handlers.address_query_handler import AddressQueryHandler
from handlers.customer_spending_handler import CustomerSpendingHandler
from handlers.total_sales_handler import TotalSalesHandler
from handlers.customers_spending_min_handler import CustomersSpendingMinHandler
from handlers.base_handler import BaseHandler
from handlers.customers_min_product_handler import CustomersMinProductsHandler
from handlers.customers_by_product_handler import CustomersByProductHandler
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

        }

    def generate(self, user_input: str) -> str:
        intent = self.classifier.classify(user_input)
        handler = self.intent_map.get(intent)
        if handler:
            return handler.handle(user_input)
        return "Sorduğunuzu anlayamadım, lütfen tekrar deneyin."
