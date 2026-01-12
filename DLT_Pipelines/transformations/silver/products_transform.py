import dlt 
from pyspark.sql.functions import *

@dlt.view(name='products_enr_view')
def products_enr_view():
  return spark.readStream.table('products_stg')\
      .withColumn('price', col('price').cast('integer'))

dlt.create_streaming_table(name='products_enr')

dlt.create_auto_cdc_flow(
    target='products_enr',
    source='products_enr_view',
    keys=['product_id'],
    sequence_by='last_updated',
    ignore_null_updates=False,
    apply_as_deletes=None,
    apply_as_truncates=None,
    column_list=None,
    except_column_list=None,
    stored_as_scd_type=1,
    track_history_column_list=None,
    track_history_except_column_list=None
)