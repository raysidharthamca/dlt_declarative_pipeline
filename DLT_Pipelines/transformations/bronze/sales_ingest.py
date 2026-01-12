import dlt

sales_rules = {
    'rules_1': 'sales_id is not null'
}

dlt.create_streaming_table(
    name='sales_stg',
    expect_all_or_drop=sales_rules
)

@dlt.append_flow(target='sales_stg')
def east_sales():
  return spark.readStream.table('dlt_sid.source.sales_east')

@dlt.append_flow(target='sales_stg')
def west_sales():
  return spark.readStream.table('dlt_sid.source.sales_west')


