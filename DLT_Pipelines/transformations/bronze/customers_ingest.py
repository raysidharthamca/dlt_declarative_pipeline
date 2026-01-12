import dlt

customers_rules = {
        'rule_1': 'customer_id is not null',
        'rule_2': 'customer_name is not null'
}

@dlt.table(name='customers_stg')
@dlt.expect_all(customers_rules)
def customers_stg():
  return spark.readStream.table('dlt_sid.source.customers')