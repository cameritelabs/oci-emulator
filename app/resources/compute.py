import string
import random

from datetime import datetime
from time import sleep
from threading import Thread
from functools import partial
from typing import List

from app.enums.compute.lifecycle_state import LifecycleState

instances = {}


def setup_instance(instance) -> None:
    sleep(2)
    instance["lifecycle_state"] = LifecycleState.PROVISIONING.value
    sleep(2)
    instance["lifecycle_state"] = LifecycleState.RUNNING.value


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
        "agent_config": {
            "are_all_plugins_disabled": False,
            "is_management_disabled": False,
            "is_monitoring_disabled": False,
            "plugins_config": [
                {"desired_state": "ENABLED", "name": "Compute Instance Monitoring"}
            ],
        },
        "availability_config": {"recovery_action": "RESTORE_INSTANCE"},
        "availability_domain": availability_domain,
        "compartment_id": compartment_id,
        "dedicated_vm_host_id": None,
        "defined_tags": {
            "Oracle-Tags": {
                "CreatedBy": "oracleidentitycloudservice/default_user",
                "CreatedOn": utc_datetime,
            }
        },
        "display_name": display_name,
        "extended_metadata": {},
        "fault_domain": "FAULT-DOMAIN-2",
        "freeform_tags": {},
        "id": instance_ocid,
        "image_id": ubuntu_image_ocid,
        "instance_options": {"are_legacy_imds_endpoints_disabled": False},
        "ipxe_script": None,
        "launch_mode": "NATIVE",
        "launch_options": {
            "boot_volume_type": "PARAVIRTUALIZED",
            "firmware": "UEFI_64",
            "is_consistent_volume_naming_enabled": True,
            "is_pv_encryption_in_transit_enabled": False,
            "network_type": "VFIO",
            "remote_data_volume_type": "PARAVIRTUALIZED",
        },
        "lifecycle_state": LifecycleState.STARTING.value,
        "metadata": {},
        "platform_config": None,
        "region": "sa-saopaulo-1",
        "shape": shape,
        "shape_config": {
            "gpu_description": None,
            "gpus": 0,
            "local_disk_description": None,
            "local_disks": 0,
            "local_disks_total_size_in_gbs": None,
            "max_vnic_attachments": 2,
            "memory_in_gbs": 1.0,
            "networking_bandwidth_in_gbps": 1.0,
            "ocpus": 1.0,
            "processor_description": "2.25 GHz AMD EPYC\u2122 7742 (Rome)",
        },
        "source_details": {
            "boot_volume_size_in_gbs": None,
            "image_id": ubuntu_image_ocid,
            "kms_key_id": None,
            "source_type": "image",
        },
        "system_tags": {},
        "time_created": utc_datetime,
        "time_maintenance_reboot_due": None,
    }

    instances[instance_id] = instance
    _setup_instance = partial(setup_instance, instance)
    Thread(target=_setup_instance).start()

    return instance


def get_instances() -> List[dict]:
    return list(instances.values())


def delete_instance(instance_id) -> None:
    del instances[instance_id]