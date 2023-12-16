import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node PostgreSQL
PostgreSQL_node1702759080295 = glueContext.create_dynamic_frame.from_options(
    connection_type="postgresql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "medical_information",
        "connectionName": "Postgresql connection",
    },
    transformation_ctx="PostgreSQL_node1702759080295",
)

# Script generated for node SQL Query
SqlQuery967 = """
select * from myDataSource
"""
SQLQuery_node1702759249015 = sparkSqlQuery(
    glueContext,
    query=SqlQuery967,
    mapping={"myDataSource": PostgreSQL_node1702759080295},
    transformation_ctx="SQLQuery_node1702759249015",
)

# Script generated for node Amazon S3
AmazonS3_node1702759305383 = glueContext.write_dynamic_frame.from_options(
    frame=SQLQuery_node1702759249015,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://jasonwang-insurance-bucket/data/",
        "partitionKeys": [],
    },
    format_options={"compression": "snappy"},
    transformation_ctx="AmazonS3_node1702759305383",
)

job.commit()
