from pypika import Query, Table, functions as fn
from pypika.terms import Order

class QueryBuilder:
    def __init__(self):
        self.customers = Table("customers")
        self.invoices = Table("invoices")
        self.invoice_lines = Table("invoice_lines")

    def get_customers_by_city(self, city: str) -> str:
        normalized_city = city.replace("İ", "i").lower()
        q = Query.from_(self.customers) \
            .select(self.customers.name, self.customers.address) \
            .where(self.customers.address.ilike(f'%{normalized_city}%')) \
            .orderby(self.customers.name)
        return str(q)

    def get_total_sales(self) -> str:
        q = Query.from_(self.invoices).select(fn.Sum(self.invoices.total_amount))
        return str(q)

    def get_customer_total_spending(self, customer_name: str) -> str:
        q = Query.from_(self.customers) \
            .join(self.invoices).on(self.customers.customer_id == self.invoices.customer_id) \
            .select(self.customers.name, fn.Sum(self.invoices.total_amount).as_('total_spent')) \
            .where(self.customers.name == customer_name) \
            .groupby(self.customers.name)
        return str(q)

    def get_top_spending_customers(self, limit: int = 5) -> str:
        q = Query.from_(self.invoices) \
            .join(self.customers).on(self.customers.customer_id == self.invoices.customer_id) \
            .select(self.customers.name, fn.Sum(self.invoices.total_amount).as_('total_spent')) \
            .groupby(self.customers.name) \
            .orderby(fn.Sum(self.invoices.total_amount), order=Order.desc) \
            .limit(limit)
        return str(q)

    def get_sales_by_date(self, date_str: str) -> str:
        q = Query.from_(self.invoices) \
            .select(fn.Sum(self.invoices.total_amount)) \
            .where(self.invoices.invoice_date == date_str)
        return str(q)

    def get_customer_product_quantity(self, customer_name: str, product_name: str) -> str:
        q = Query.from_(self.customers) \
            .join(self.invoices).on(self.customers.customer_id == self.invoices.customer_id) \
            .join(self.invoice_lines).on(self.invoices.invoice_id == self.invoice_lines.invoice_id) \
            .select(self.customers.name, fn.Sum(self.invoice_lines.quantity).as_('total_quantity')) \
            .where(self.customers.name == customer_name) \
            .where(self.invoice_lines.product_name.ilike(f'%{product_name}%')) \
            .groupby(self.customers.name, self.invoice_lines.product_name)
        return str(q)
    

    def get_all_product_names(self) -> str:
        q = Query.from_(self.invoice_lines).select(self.invoice_lines.product_name).distinct()
        return str(q)

    def get_customers_with_minimum_products(self, min_products: int = 3) -> str:
        # COUNT(DISTINCT invoice_lines.product_name) AS product_count
        distinct_count = fn.Count(self.invoice_lines.product_name).distinct().as_('product_count')

        q = (
            Query
            .from_(self.invoice_lines)
            .join(self.invoices).on(self.invoice_lines.invoice_id   == self.invoices.invoice_id)
            .join(self.customers).on(self.invoices.customer_id     == self.customers.customer_id)
            .select(self.customers.name, distinct_count)
            .groupby(self.customers.name)
            .having(fn.Count(self.invoice_lines.product_name).distinct() >= min_products)
        )
        return str(q)