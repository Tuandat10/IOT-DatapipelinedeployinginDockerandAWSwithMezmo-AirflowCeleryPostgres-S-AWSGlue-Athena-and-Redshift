import sys
import json
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, explode, from_json, schema_of_json

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load CSV from S3
source_df = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://mezmo-data-engineering/raw_full_log/"], "recurse": True},
    transformation_ctx="source_df"
).toDF()

# Get first non-null message to infer JSON schema
sample_json_str = source_df.select("message").rdd.map(lambda row: row[0]).filter(lambda x: x is not None).first()
json_schema = schema_of_json(sample_json_str)

# Parse the message JSON array
parsed_df = source_df.withColumn("message_array", from_json(col("message"), json_schema))

# Explode array into multiple rows
exploded_df = parsed_df.withColumn("log", explode(col("message_array")))

# Flatten the exploded JSON fields
flattened_df = exploded_df.select(
    "host",
    "timestamp",
    "level",
    "error_event",
    "error_type",
    col("log.message").alias("log_message"),
    col("log.timestamp").alias("log_timestamp"),
    col("log.level").alias("log_level")
)

# Write to S3 in parquet format
flattened_dynamic_df = DynamicFrame.fromDF(flattened_df, glueContext, "flattened_dynamic_df")
glueContext.write_dynamic_frame.from_options(
    frame=flattened_dynamic_df,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://mezmo-data-engineering/tranformed_mezmo/", "partitionKeys": []},
    format_options={"compression": "snappy"},
    transformation_ctx="output"
)

job.commit()
