from typing import Optional

from oci.core import ComputeClient, ComputeClientCompositeOperations
from oci.core.models import LaunchInstanceDetails
from oci.core.models.instance import Instance
from oci.response import Response


def create_instance(
    compartment_id: str,
    compute_client_composite_op: ComputeClientCompositeOperations,
    instance_name: Optional[str] = None,
) -> Instance:
    launch_instance_details = LaunchInstanceDetails(
        availability_domain="utiT:SA-SAOPAULO-1-AD-1",
        compartment_id=compartment_id,
        shape="VM.Standard.E3.Flex",
        display_name=instance_name,
    )
    response: Response = compute_client_composite_op.launch_instance_and_wait_for_state(
        launch_instance_details, wait_for_states=[Instance.LIFECYCLE_STATE_RUNNING]
    )

    return response.data


def terminate_instance(instance_id: str, compute_client: ComputeClient) -> None:
    compute_client.terminate_instance(instance_id)
