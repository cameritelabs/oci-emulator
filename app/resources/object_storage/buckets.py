import uuid
import random
import string
import datetime

buckets = []


def create_bucket(namespace, userId, bucket):
    random_60_digits = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=60)
    )

    new_bucket = {
        "approximateCount": 0,
        "approximateSize": 0,
        "compartmentId": bucket["compartmentId"],
        "createdBy": userId,
        "definedTags": bucket["definedTags"] if "definedTags" in bucket else None,
        "etag": str(uuid.uuid4()),
        "freeformTags": bucket["freeformTags"] if "freeformTags" in bucket else None,
        "id": "ocid1.bucket.oc1.sa-saopaulo-1." + random_60_digits,
        "isReadOnly": None,
        "kmsKeyId": None,
        "metadata": None,
        "name": bucket["name"],
        "namespace": namespace,
        "objectEventsEnabled": None,
        "objectLifecyclePolicyEtag": None,
        "publicAccessType": bucket["publicAccessType"]
        if "publicAccessType" in bucket
        else None,
        "replicationEnabled": None,
        "storageTier": bucket["storageTier"] if "storageTier" in bucket else None,
        "timeCreated": datetime.datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%S.%f+00:00"
        ),
        "versioning": "Disabled",
    }

    buckets.append(new_bucket)
    return new_bucket


def list_buckets(namespace, compartment_id):
    return [
        bucket
        for bucket in buckets
        if bucket["compartmentId"] == compartment_id
        and bucket["namespace"] == namespace
    ]
