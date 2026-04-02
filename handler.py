import json
import logging
import os
import boto3
from shapely.geometry import shape

_sm = boto3.client("secretsmanager")
s3 = boto3.client("s3")


def lambda_handler(event, context):
    secret_id = os.environ["EARTHONE_SECRET_ID"]
    secrets = _sm.get_secret_value(SecretId=secret_id)
    secrets_json = json.loads(secrets["SecretString"])

    os.environ["EARTHONE_CLIENT_ID"] = secrets_json["client_id"]
    os.environ["EARTHONE_CLIENT_SECRET"] = secrets_json["client_secret"]
    import earthdaily.earthone as eo

    tiff_key = event["tiff_key"]
    bucket = event["bucket"]
    metadata = event["metadata"]

    head = s3.head_object(Bucket=event["bucket"], Key=tiff_key)
    if head["ContentLength"] <= 0:
        raise ValueError(f"Image file is empty: {tiff_key}")
    
    local_path = f"/tmp/{os.path.basename(tiff_key)}"
    s3.download_file(bucket, tiff_key, local_path)

    product = eo.catalog.Product.get_or_create("earthdaily:maxar-gegd-rgb:v1")
    product.save()

    image = eo.catalog.Image(id = product.named_id(metadata["id"]))
    image.product = product
    image.geometry = metadata["aoi"]
    image.acquired = metadata["start_date"]
    image.acquired_end = metadata["stop_date"]

    upload = image.upload(local_path)
    upload.wait_for_completion()

    if metadata["aoi"]:
        metadata["aoi"] = shape(metadata["aoi"]).wkt

    return {
        "metadata": metadata
    }

