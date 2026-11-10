"""Session Spark configurée pour Delta Lake + RustFS (S3A) + PostgreSQL (JDBC)."""
import os
import sys

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
    # Spark 3.5 exige Java 17 (ou 11) : si le Java du PC est plus récent (21, 25...),
    # indiquer le dossier d'un JDK 17 dans SPARK_JAVA_HOME (fichier .env).
    java_home = os.getenv("SPARK_JAVA_HOME")
    if java_home:
        os.environ["JAVA_HOME"] = java_home
        os.environ["PATH"] = os.path.join(java_home, "bin") + os.pathsep + os.environ.get("PATH", "")
    # Windows : Hadoop a besoin de winutils.exe et hadoop.dll dans %HADOOP_HOME%\bin
    hadoop_home = os.getenv("HADOOP_HOME")
    if hadoop_home:
        os.environ["PATH"] = os.path.join(hadoop_home, "bin") + os.pathsep + os.environ.get("PATH", "")
    # Les workers Python doivent utiliser le même interpréteur que le notebook (.venv)
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)
    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "4g"))
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.jars.packages", PACKAGES)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.hadoop.fs.s3a.endpoint", config.RUSTFS_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", config.RUSTFS_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", config.RUSTFS_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        # Adresse locale explicite : évite les blocages de résolution de nom (Windows, VPN)
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
        # Échec rapide si RustFS ne répond pas (par défaut : plusieurs minutes de tentatives)
        .config("spark.hadoop.fs.s3a.connection.establish.timeout", "5000")
        .config("spark.hadoop.fs.s3a.connection.timeout", "30000")
        .config("spark.hadoop.fs.s3a.attempts.maximum", "3")
        .config("spark.hadoop.fs.s3a.retry.limit", "3")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
