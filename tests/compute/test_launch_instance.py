from unittest import TestCase

from oci.core import ComputeClient, ComputeClientCompositeOperations
from oci.core.models import LaunchInstanceDetails
from oci.core.models.instance import Instance
from oci.response import Response
from oci.exceptions import ServiceError

from oci_emulator import app
from tests import get_oci_config, ServerThread
from tests.compute import terminate_instance


class ComputeClientLaunchInstance(TestCase):
    def setUp(self):
        self.server = ServerThread(app)
        self.server.start()
        self.oci_config = get_oci_config()
        self.compute_cli = ComputeClient(
            config=self.oci_config["config"], service_endpoint="http://localhost:12000"
        )
        self.compute_cli_composite_op = ComputeClientCompositeOperations(
            self.compute_cli
        )
        self.created_instances = []

    def test_launch_instance(self):
        launch_instance_details = LaunchInstanceDetails(
            availability_domain="utiT:SA-SAOPAULO-1-AD-1",
            compartment_id=self.oci_config["compartment_id"],
            shape="VM.Standard.E3.Flex",
            display_name="dummy-instance",
        )
        response: Response = (
            self.compute_cli_composite_op.launch_instance_and_wait_for_state(
                launch_instance_details,
                wait_for_states=[Instance.LIFECYCLE_STATE_RUNNING],
            )
        )

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.data, Instance)

        instance: Instance = response.data
        self.created_instances.append(instance)

        self.assertEqual(instance.availability_domain, "utiT:SA-SAOPAULO-1-AD-1")
        self.assertEqual(instance.compartment_id, self.oci_config["compartment_id"])
        self.assertEqual(instance.shape, "VM.Standard.E3.Flex")
        self.assertEqual(instance.display_name, "dummy-instance")

    def test_launch_instance_bad_requests(self):
        wrong_launch_instance_details = [
            LaunchInstanceDetails(
                availability_domain="utiT:SA-SAOPAULO-1-AD-1",
                compartment_id=self.oci_config["compartment_id"],
            ),
            LaunchInstanceDetails(
                availability_domain="utiT:SA-SAOPAULO-1-AD-1",
                shape="VM.Standard.E3.Flex",
            ),
            LaunchInstanceDetails(
                compartment_id=self.oci_config["compartment_id"],
                shape="VM.Standard.E3.Flex",
            ),
        ]

        for launch_instance_details in wrong_launch_instance_details:
            with self.assertRaises(ServiceError) as e:
                self.compute_cli_composite_op.launch_instance_and_wait_for_state(
                    launch_instance_details,
                    wait_for_states=[Instance.LIFECYCLE_STATE_RUNNING],
                )

                self.assertEqual(e.exception.status == 400)

    def tearDown(self):
        for instance in self.created_instances:
            terminate_instance(instance.id, self.compute_cli)

        self.server.shutdown()
