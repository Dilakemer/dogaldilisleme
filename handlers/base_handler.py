from abc import ABC, abstractmethod
from typing import Optional
from db.query_builder import QueryBuilder
from db.connection import run_query
from services.intent_classifier import IntentClassifier

class BaseHandler(ABC):
    def __init__(self, query_builder: QueryBuilder, classifier: IntentClassifier):
        self.query_builder = query_builder
        self.classifier = classifier

    @abstractmethod
    def handle(self, text: str) -> str:
        min_products = self.classifier.extract_min_products(text)
        self.classifier.log(f"Extracted min_products: {min_products}")
        query = self.query_builder.get_customers_with_minimum_products(min_products)
        self.classifier.log(f"Generated SQL: {query}")
        result = run_query(query)
        self.classifier.log(f"Query result: {result}")
