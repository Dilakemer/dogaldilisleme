from typing import Optional
import re
from db.connection import run_query
from db.query_builder import QueryBuilder
from services.intent_classifier import IntentClassifier
from services.questions_db import QUESTIONS_ANSWERS
from services.similarity_search import find_similar_question

class ResponseGenerator:
    def __init__(self, products: Optional[list] = None, debug: bool = False):
        self.classifier = IntentClassifier(products=products, debug=debug)
        self.query_builder = QueryBuilder()

    def generate(self, user_input: str) -> str:
        intent = self.classifier.classify(user_input)

        if intent == "address_query":
            city = self.classifier.extract_city(user_input)
            if city:
                query = self.query_builder.get_customers_by_city(city)
                result = run_query(query)
                if result:
                    customers = "\n".join([f"- {row[0]} ({row[1]})" for row in result])
                    return f"{city} şehrindeki müşteriler:\n{customers}\n\n[Oluşturulan SQL sorgusu]:\n{query}"
                return f"{city} şehrinde müşteri bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return "Şehir adı algılanamadı."

        elif intent == "total_sales":
            query = self.query_builder.get_total_sales()
            result = run_query(query)
            if result and result[0][0] is not None:
                return f"Toplam satış tutarı: {result[0][0]:,.2f} ₺\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return f"Toplam satış bilgisi bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"

        elif intent == "customer_spending":
            customer_name = self.classifier.extract_customer_name(user_input)
            if customer_name:
                query = self.query_builder.get_customer_total_spending(customer_name)
                result = run_query(query)
                if result and result[0][1] is not None:
                    return f"{customer_name} toplamda {result[0][1]:,.2f} ₺ harcamış.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
                return f"{customer_name} adlı müşteri için harcama verisi bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return "Müşteri adı algılanamadı."

        elif intent == "top_spenders":
            query = self.query_builder.get_top_spending_customers()
            result = run_query(query)
            if result:
                top_list = "\n".join([f"- {row[0]}: {row[1]:,.2f} ₺" for row in result])
                return f"En çok harcama yapan müşteriler:\n{top_list}\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return f"Hiçbir müşteri verisi bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"

        elif intent == "customers_by_product":
            product = self.classifier.extract_product(user_input)
            if not product:
                return "Hangi ürün olduğunu anlayamadım, lütfen tekrar belirtin."
            query = self.query_builder.get_customers_by_product(product)
            result = run_query(query)
            if result:
                lines = "\n".join([f"- {r[0]} ({r[1]})" for r in result])
                return f"Faturalarında '{product}' geçen müşteriler:\n{lines}\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return f"Faturalarında '{product}' geçen müşteri bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"

        elif intent == "sales_on_date":
            date = self.classifier.extract_date(user_input)
            if date:
                query = self.query_builder.get_sales_by_date(date)
                result = run_query(query)
                if result and result[0][0] is not None:
                    return f"{date} tarihindeki toplam satış: {result[0][0]:,.2f} ₺\n\n[Oluşturulan SQL sorgusu]:\n{query}"
                return f"{date} tarihine ait satış bilgisi bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return "Tarih algılanamadı."

        elif intent == "customers_min_products":
            min_products = self._extract_min_products(user_input)
            query = self.query_builder.get_customers_with_minimum_products(min_products)
            result = run_query(query)
            if result:
                response_list = "\n".join([f"- {row[0]}: {row[1]} farklı ürün" for row in result])
                return f"En az {min_products} farklı ürün satın alan müşteriler:\n{response_list}\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return f"Hiçbir müşteri en az {min_products} farklı ürün satın almamış.\n\n[Oluşturulan SQL sorgusu]:\n{query}"

        elif intent == "customer_product_quantity":
            customer_name = self.classifier.extract_customer_name(user_input)
            product_name, quantity = self.classifier.extract_product_quantity(user_input)
            if customer_name and product_name:
                query = self.query_builder.get_customer_product_quantity(customer_name, product_name)
                result = run_query(query)
                if result and result[0][1] is not None:
                    return f"{customer_name} toplamda {result[0][1]} adet {product_name} aldı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
                return f"{customer_name} adlı müşteri için {product_name} ürünü bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"
            return "Müşteri veya ürün adı algılanamadı."

        else:
            return "Sorduğunuzu anlayamadım, lütfen tekrar deneyin."


    def generate_with_similarity(self, user_input: str) -> str:
        questions = QUESTIONS_ANSWERS.questions
        match, score = find_similar_question(user_input, questions)
        if match:
            return f"Bunu mu demek istediniz? '{match}'"
        return "Üzgünüm, sorunuza benzer bir kayıt bulunamadı."

    def generate_with_similarity_with_sql(self, user_input: str) -> str:
        # Yalnızca öneri aşamasında kullanılır, detaylı cevap vermez
        questions = QUESTIONS_ANSWERS.questions
        match, score = find_similar_question(user_input, questions)
        if not match:
            return "Üzgünüm, sorunuza benzer bir kayıt bulunamadı."
        return f"Bunu mu demek istediniz: '{match}'?"

    def generate_final_answer_with_sql(self, match: str) -> str:
        questions = QUESTIONS_ANSWERS.questions
        answers = QUESTIONS_ANSWERS.answers

        if match not in questions:
            return "Üzgünüm, eşleşen bir kayıt bulunamadı."

        idx = questions.index(match)
        intent = self.classifier.classify(match)

        # SQL üretimi intent'e göre yapılır
        if intent == "total_sales":
            sql_query = self.query_builder.get_total_sales()
            result = run_query(sql_query)
            dynamic_answer = (
                f"Toplam satış tutarı: {result[0][0]:,.2f} ₺" if result and result[0][0] else "Satış verisi bulunamadı."
            )

        elif intent == "customers_min_products":
            min_products = self._extract_min_products(match)
            sql_query = self.query_builder.get_customers_with_minimum_products(min_products)
            result = run_query(sql_query)
            if result:
                dynamic_answer = "\n".join([f"- {row[0]}: {row[1]} farklı ürün" for row in result])
            else:
                dynamic_answer = f"En az {min_products} farklı ürün alan müşteri bulunamadı."

        elif intent == "customers_by_product":
            product = self.classifier.extract_product(match)
            if product:
                sql_query = self.query_builder.get_customers_by_product(product)
                result = run_query(sql_query)
                if result:
                    dynamic_answer = "\n".join([f"- {row[0]} ({row[1]})" for row in result])
                else:
                    dynamic_answer = f"'{product}' içeren fatura bulunamadı."
            else:
                sql_query = "-- Ürün bulunamadı --"
                dynamic_answer = "Ürün ismi algılanamadı."

        else:
            sql_query = "-- Sorgu bulunamadı --"
            dynamic_answer = "Bu soruya karşılık gelen sorgu tanımlı değil."

        return (
            f"Soru: {match}\n"
            f"Cevap:\n{dynamic_answer}\n\n"
            f"[Oluşturulan SQL sorgusu]:\n{sql_query}"
        )


    @staticmethod
    def _extract_min_products(text: str) -> int:
        match = re.search(r'en az (\d+)', text.lower())
        return int(match.group(1)) if match else 1
    def generate_with_sql(self, user_input: str) -> str:
        intent = self.classifier.classify(user_input)

        if intent == "customers_min_products":
            min_products = self._extract_min_products(user_input)
            query = self.query_builder.get_customers_with_minimum_products(min_products)
            result = run_query(query)
            if result:
                response_list = "\n".join([f"- {row[0]}: {row[1]} farklı ürün" for row in result])
                return (
                    f"En az {min_products} farklı ürün satın alan müşteriler:\n{response_list}\n\n"
                    f"[Oluşturulan SQL sorgusu]:\n{query}"
                )
            return f"Hiçbir müşteri en az {min_products} farklı ürün satın almamış.\n\n[Oluşturulan SQL sorgusu]:\n{query}"

        elif intent == "customers_by_product":
            product = self.classifier.extract_product(user_input)
            query = self.query_builder.get_customers_by_product(product)
            result = run_query(query)
            if result:
                customer_lines = "\n".join([f"- {row[0]} ({row[1]})" for row in result])
                return (
                    f"Faturalarında '{product}' geçen müşteriler:\n{customer_lines}\n\n"
                    f"[Oluşturulan SQL sorgusu]:\n{query}"
                )
            return f"'{product}' içeren fatura bulunamadı.\n\n[Oluşturulan SQL sorgusu]:\n{query}"

        return self.generate(user_input)
