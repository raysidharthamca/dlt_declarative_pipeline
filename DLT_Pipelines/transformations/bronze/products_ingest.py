import dlt

products_rules = {
        'rule_1': 'product_id is not null',
        'rule_2': 'price >= 0'
}

@dlt.table(name='products_stg')
@dlt.expect_all(products_rules)
def products():
  return spark.readStream.table('dlt_sid.source.products')

