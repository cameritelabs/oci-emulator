import uuid
import random
import string
import datetime

buckets = []


def create_bucket(namespace, userId, bucket):
    random_60_digits = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=60)
    )

    for existing_bucket in buckets:
        if (
            bucket["namespace"] == namespace
            and existing_bucket["name"] == bucket["name"]
        ):
            return False, "already_exists"

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
        "_objects": [],
    }

    buckets.append(new_bucket)
    return True, new_bucket


def list_buckets(namespace, compartment_id):
    return [
        bucket
        for bucket in buckets
        if bucket["compartmentId"] == compartment_id
        and bucket["namespace"] == namespace
    ]


def remove_bucket(namespace, bucket_name):
    for bucket in buckets:
        if bucket["namespace"] == namespace and bucket["name"] == bucket_name:

            if len(bucket["_objects"]) > 0:
                return False, "has_objects"

            buckets.remove(bucket)
            return True, None

    return False, "not_found"
