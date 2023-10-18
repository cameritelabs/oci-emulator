import datetime
import random
import string

queues = []


def add_queue(queue):
    global queues
    random_60_digits = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=60)
    )

    queues.append(
        {
            "id": "ocid1.queue.oc1.sa-saopaulo-1." + random_60_digits,
            "displayName": queue["displayName"],
            "compartmentId": queue["compartmentId"],
            "timeCreated": datetime.datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%f+00:00"
            ),
            "timeUpdated": datetime.datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%f+00:00"
            ),
            "lifecycleState": "ACTIVE",
            "lifecycleDetails": None,
            "messagesEndpoint": "http://localhost:12000",
            # this is not returned by list method
            "retentionInSeconds": 86400,
            "visibilityInSeconds": 30,
            "timeoutInSeconds": 30,
            "deadLetterQueueDeliveryCount": 0,
            "customEncryptionKeyId": None,
            "channelConsumptionLimit": 100,
            # tags
            "capabilities": [],
            "freeformTags": {},
            "definedTags": {},
            "systemTags": {},
        }
    )


def list_queues(compartment_id, lifecycle_state=None):
    global queues
    returned_queues = []

    for queue in queues:
        if queue["compartmentId"] != compartment_id:
            continue

        if lifecycle_state and queue["lifecycleState"] != lifecycle_state:
            continue

        returned_queues.append(queue)

    return returned_queues


def get_queue_by_id(queue_id):
    global queues
    for queue in queues:
        if queue["id"] == queue_id:
            return queue
    return None


def delete_queue(queue_id):
    global queues
    for queue in queues:
        if queue["id"] == queue_id:
            queue["lifecycleState"] = "DELETED"
            queue["timeUpdated"] = datetime.datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%f+00:00"
            )

            return True, None

    return False, "not_found"
