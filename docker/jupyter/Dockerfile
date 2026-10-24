# JupyterLab + PySpark 3.5 (compatible Delta Lake 3.2 et hadoop-aws 3.3.4)
FROM quay.io/jupyter/pyspark-notebook:spark-3.5.3

USER root
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
USER ${NB_UID}

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Les JARs (Delta, S3A) sont téléchargés par Spark au premier lancement
# via spark.jars.packages (cf. src/spark_session.py)
ENV PYTHONPATH=/home/jovyan/work/src
EXPOSE 8888 4040
