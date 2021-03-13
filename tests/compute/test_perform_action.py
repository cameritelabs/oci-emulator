from typing import List
from unittest import TestCase

from oci.core import ComputeClient, ComputeClientCompositeOperations
from oci.core.models.instance import Instance
from oci.response import Response
from oci.exceptions import ServiceError

from oci_emulator import app
from app.enums.compute.instance_action import InstanceAction
from tests import get_oci_config, ServerThread
from tests.compute import create_instance, terminate_instance


class ComputeClientRoutes(TestCase):
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

        self.test_instance = create_instance(
            self.oci_config["compartment_id"],
            self.compute_cli_composite_op,
            "dummy-instance",
        )

    def test_perform_action(self):
        response: Response = self.compute_cli.list_instances(
            self.oci_config["compartment_id"], display_name="dummy-instance"
        )
        instances: List[Instance] = response.data
        test_instance = instances[0]

        for action in list(InstanceAction.__members__.keys()):
            response: Response = self.compute_cli.instance_action(
                test_instance.id, action=action
            )

            assert response.status == 200
            assert response.data
            assert response.data.id == test_instance.id

    def test_perform_action_on_nonexistent_instance(self):
        with self.assertRaises(ServiceError) as e:
            self.compute_cli.instance_action("non_existent_instance", action="RESET")
            self.assertEqual(e.exception.status, 404)

    def test_perform_invalid_action(self):
        with self.assertRaises(ServiceError) as e:
            self.compute_cli.instance_action("dummy-instance", action="CRAZY_DUDE")
            self.assertEqual(e.exception.status, 404)

    def tearDown(self):
        terminate_instance(self.test_instance.id, self.compute_cli)
        self.server.shutdown()
