from db.query_builder import QueryBuilder
qb = QueryBuilder()
print(qb.get_customers_by_city("İzmir"))
print(qb.get_total_sales())
print(qb.get_customer_total_spending("Alice Johnson"))
print(qb.get_top_spending_customers())
print(qb.get_sales_by_date("2023-07-01"))
print(qb.get_customer_product_quantity("Alice Johnson", "Cheese"))
