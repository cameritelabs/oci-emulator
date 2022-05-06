import string
import random

from datetime import datetime
from time import sleep
from threading import Thread
from functools import partial
from typing import List, Optional

from app.enums.compute.instance_action import InstanceAction
from app.enums.compute.lifecycle_state import LifecycleState

instances = {}


def _change_instance_status(instance: dict, status_order: List[LifecycleState]) -> None:
    for status in status_order:
        sleep(1)  # Maybe this sleep time should be configurable
        instance["lifecycleState"] = status.value


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

    name = kwargs.get("display_name")

    if name:
        display_name = name

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
    _setup_instance = partial(
        _change_instance_status,
        instance,
        [LifecycleState.PROVISIONING, LifecycleState.RUNNING],
    )
    Thread(target=_setup_instance).start()

    return instance


def find_instance(instance_ocid: str) -> Optional[dict]:
    if instance_ocid in instances:
        return instances[instance_ocid]

    return None


def get_instances(params: Optional[dict] = None) -> List[dict]:
    instances_to_return = []

    for instance in instances.values():
        should_add = True

        if params:
            for param in params.keys():
                if params[param] and instance[param] not in params[param]:
                    should_add = False
                    break

        if should_add:
            instances_to_return.append(instance)

    return instances_to_return


def terminate_instance(instance_ocid: str) -> None:
    instance = instances[instance_ocid]
    _change_instance_status(
        instance, [LifecycleState.TERMINATING, LifecycleState.TERMINATED]
    )

    while True:
        if instance["lifecycleState"] == LifecycleState.TERMINATED.value:
            del instances[instance_ocid]
            break


def instance_action(instance_ocid: str, action: InstanceAction) -> None:
    _perform_action = partial(
        _change_instance_status, instances[instance_ocid], action.value
    )
    Thread(target=_perform_action).start()
