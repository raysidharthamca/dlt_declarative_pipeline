'''
import dlt
from pyspark.sql.functions import *

@dlt.table(name='staging_orders')
def staging_orders():
  return spark.readStream.table('dlt_sid.source.orders')

@dlt.view(name='tranformed_orders')
def tranformed_orders():
    df = dlt.read_stream('staging_orders')\
            .withColumn('order_status', lower(col('order_status')))
    return df
    
@dlt.table(name='aggregated_orders')
def aggregated_orders():
    df = dlt.readStream('tranformed_orders')\
            .groupBy(col('order_status'))\
            .agg(count('*').alias('order_count'))
    return df
'''