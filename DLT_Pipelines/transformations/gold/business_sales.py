import dlt

@dlt.table(name='business_sales')
def business_sales():
  return spark.sql('''
    SELECT 
        region,
        category,
        SUM(amount) as total_sales 
    FROM 
        fact_sales sales join dim_customers cust 
            on sales.customer_id = cust.customer_id
        join dim_products prod 
            on sales.product_id = prod.product_id 
    GROUP BY
        region,
        category
    ''')