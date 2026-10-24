"""Utilitaire : crée le bucket du data lake dans RustFS s'il n'existe pas.

À appeler au début du notebook 01 :
    from lake import creer_bucket
    creer_bucket()
"""
import boto3
from botocore.exceptions import ClientError

import config


def creer_bucket() -> None:
    s3 = boto3.client(
        "s3",
        endpoint_url=config.RUSTFS_ENDPOINT,
        aws_access_key_id=config.RUSTFS_ACCESS_KEY,
        aws_secret_access_key=config.RUSTFS_SECRET_KEY,
    )
    try:
        s3.head_bucket(Bucket=config.LAKE_BUCKET)
        print(f"Bucket '{config.LAKE_BUCKET}' déjà présent")
    except ClientError:
        s3.create_bucket(Bucket=config.LAKE_BUCKET)
        print(f"Bucket '{config.LAKE_BUCKET}' créé")
