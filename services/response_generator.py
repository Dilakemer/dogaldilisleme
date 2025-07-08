from typing import Optional
from db.connection import run_query
from db.query_builder import QueryBuilder
from services.intent_classifier import IntentClassifier


class ResponseGenerator:
    def __init__(self, products: Optional[list] = None, debug: bool = False):
        self.classifier = IntentClassifier(products=products, debug=debug)
        self.query_builder = QueryBuilder()  # QueryBuilder nesnesi

    def generate(self, user_input: str) -> str:
        intent = self.classifier.classify(user_input)

        if intent == "address_query":
            city = self.classifier.extract_city(user_input)
            if city:
                query = self.query_builder.get_customers_by_city(city)
                result = run_query(query)
                if result:
                    customers = "\n".join([f"- {row[0]} ({row[1]})" for row in result])
                    return f"{city} şehrindeki müşteriler:\n{customers}"
                else:
                    return f"{city} şehrinde müşteri bulunamadı."
            return "Şehir adı algılanamadı."

        elif intent == "total_sales":
            query = self.query_builder.get_total_sales()
            result = run_query(query)
            if result and result[0][0] is not None:
                return f"Toplam satış tutarı: {result[0][0]:,.2f} ₺"
            else:
                return "Toplam satış bilgisi bulunamadı."

        elif intent == "customer_spending":
            customer_name = self.classifier.extract_customer_name(user_input)
            if customer_name:
                query = self.query_builder.get_customer_total_spending(customer_name)
                result = run_query(query)
                if result and result[0][1] is not None:
                    return f"{customer_name} toplamda {result[0][1]:,.2f} ₺ harcamış."
                else:
                    return f"{customer_name} adlı müşteri için harcama verisi bulunamadı."
            return "Müşteri adı algılanamadı."

        elif intent == "top_spenders":
            query = self.query_builder.get_top_spending_customers()
            result = run_query(query)
            if result:
                top_list = "\n".join([f"- {row[0]}: {row[1]:,.2f} ₺" for row in result])
                return f"En çok harcama yapan müşteriler:\n{top_list}"
            else:
                return "Hiçbir müşteri verisi bulunamadı."

        elif intent == "sales_on_date":
            date = self.classifier.extract_date(user_input)
            if date:
                query = self.query_builder.get_sales_by_date(date)
                result = run_query(query)
                if result and result[0][0] is not None:
                    return f"{date} tarihindeki toplam satış: {result[0][0]:,.2f} ₺"
                else:
                    return f"{date} tarihine ait satış bilgisi bulunamadı."
            return "Tarih algılanamadı."

        elif intent == "customers_min_products":
            min_products = self.classifier.extract_min_products(user_input)
            query = self.query_builder.get_customers_with_minimum_products(min_products)
            result = run_query(query)
            if result:
                response_list = "\n".join([f"- {row[0]}: {row[1]} farklı ürün" for row in result])
                return f"En az {min_products} farklı ürün satın alan müşteriler:\n{response_list}"
            else:
                return f"Hiçbir müşteri en az {min_products} farklı ürün satın almamış."

        elif intent == "customer_product_quantity":
            customer_name = self.classifier.extract_customer_name(user_input)
            product_name, quantity = self.classifier.extract_product_quantity(user_input)

            if customer_name and product_name:
                query = self.query_builder.get_customer_product_quantity(customer_name, product_name)
                result = run_query(query)
                if result and result[0][1] is not None:
                    return f"{customer_name} toplamda {result[0][1]} adet {product_name} aldı."
                else:
                    return f"{customer_name} adlı müşteri için {product_name} ürünü bulunamadı."
            return "Müşteri veya ürün adı algılanamadı."

        else:
            return "Sorduğunuzu anlayamadım, lütfen tekrar deneyin."
