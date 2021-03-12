import string
import random

from datetime import datetime
from time import sleep
from threading import Thread
from functools import partial
from typing import List, Optional

from app.enums.compute.lifecycle_state import LifecycleState

instances = {}


def _terminate_instance(instance) -> None:
    status_order = [LifecycleState.TERMINATING.value, LifecycleState.TERMINATED.value]

    for status in status_order:
        sleep(1)  # Maybe this sleep time should be configurable
        instance["lifecycleState"] = status


def setup_instance(instance) -> None:
    status_order = [LifecycleState.PROVISIONING.value, LifecycleState.RUNNING.value]

    for status in status_order:
        sleep(1)  # Maybe this sleep time should be configurable
        instance["lifecycleState"] = status


def create_instance(
    availability_domain: str, compartment_id: str, shape: str, **kwargs
) -> dict:
    ubuntu_image_ocid = "ocid1.image.oc1.sa-saopaulo-1.aaaaaaaandbj5tu656nigjgejj2xudkuywlk7t37aft5uki72l5y3fr4yimq"
    instance_id = "".join(
        random.choices((string.ascii_lowercase + string.digits), k=60)
    )
    instance_ocid = f"ocid1.instance.oc1.sa-saopaulo-1.{instance_id}"
    utc_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    display_name = f"instance_{instance_id}"

    if kwargs.get("display_name"):
        display_name = kwargs.get("display_name")

    instance = {
        "agentConfig": {
            "areAllPluginsDisabled": False,
            "isManagementDisabled": False,
            "isMonitoringDisabled": False,
            "pluginsConfig": [
                {"desiredState": "ENABLED", "name": "Compute Instance Monitoring"}
            ],
        },
        "availabilityConfig": {"recoveryAction": "RESTORE_INSTANCE"},
        "availabilityDomain": availability_domain,
        "compartmentId": compartment_id,
        "dedicatedVmHostId": None,
        "definedTags": {
            "Oracle-Tags": {
                "CreatedBy": "oracleidentitycloudservice/default_user",
                "CreatedOn": utc_datetime,
            }
        },
        "displayName": display_name,
        "extendedMetadata": {},
        "faultDomain": "FAULT-DOMAIN-2",
        "freeformTags": {},
        "id": instance_ocid,
        "imageId": ubuntu_image_ocid,
        "instanceOptions": {"are_legacy_imds_endpoints_disabled": False},
        "ipxeScript": None,
        "launchMode": "NATIVE",
        "launchOptions": {
            "bootVolumeType": "PARAVIRTUALIZED",
            "firmware": "UEFI_64",
            "isConsistentVolumeNamingEnabled": True,
            "isPvEncryptionInTransitEnabled": False,
            "networkType": "VFIO",
            "remoteDataVolumeType": "PARAVIRTUALIZED",
        },
        "lifecycleState": LifecycleState.STARTING.value,
        "metadata": {},
        "platformConfig": None,
        "region": "sa-saopaulo-1",
        "shape": shape,
        "shapeConfig": {
            "gpuDescription": None,
            "gpus": 0,
            "localDiskDescription": None,
            "localDisks": 0,
            "localDisksTotalSizeInGbs": None,
            "maxVnicAttachments": 2,
            "memoryInGbs": 1.0,
            "networkingBandwidthInGbps": 1.0,
            "ocpus": 1.0,
            "processorDescription": "2.25 GHz AMD EPYC\u2122 7742 (Rome)",
        },
        "sourceDetails": {
            "bootVolumeSizeInGbs": None,
            "imageId": ubuntu_image_ocid,
            "kmsKeyId": None,
            "sourceType": "image",
        },
        "systemTags": {},
        "timeCreated": utc_datetime,
        "timeMaintenanceRebootDue": None,
    }

    instances[instance_ocid] = instance
    _setup_instance = partial(setup_instance, instance)
    Thread(target=_setup_instance).start()

    return instance


def find_instance(instance_ocid: str) -> Optional[dict]:
    if instance_ocid in instances:
        return instances[instance_ocid]

    return None


def get_instances() -> List[dict]:
    return list(instances.values())


def terminate_instance(instance_ocid: str) -> None:
    del instances[instance_ocid]
