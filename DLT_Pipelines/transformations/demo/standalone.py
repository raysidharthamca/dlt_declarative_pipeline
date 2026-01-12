'''
import dlt

@dlt.table(name='first_stream_table')
def first_stream_table():
  return spark.readStream.table('dlt_sid.source.orders')

@dlt.table(name='second_mat_view')
def second_mat_view():
  return spark.read.table('dlt_sid.source.orders')

@dlt.view(name='third_streaming_view')
def third_streaming_view():
  return spark.readStream.table('dlt_sid.source.orders')

@dlt.view(name='fourth_batch_view')
def fourth_batch_view():
  return spark.read.table('dlt_sid.source.orders')

'''