"""Session Spark configurée pour Delta Lake + RustFS (S3A) + PostgreSQL (JDBC)."""
from pyspark.sql import SparkSession

import config

PACKAGES = ",".join(
    [
        "io.delta:delta-spark_2.12:3.2.1",
        "org.apache.hadoop:hadoop-aws:3.3.4",
        "com.amazonaws:aws-java-sdk-bundle:1.12.262",
        "org.postgresql:postgresql:42.7.4",
    ]
)


def get_spark(app_name: str = "velib") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", PACKAGES)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.hadoop.fs.s3a.endpoint", config.RUSTFS_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", config.RUSTFS_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", config.RUSTFS_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
