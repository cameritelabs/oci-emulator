from typing import List
from unittest import TestCase

from oci.core import ComputeClient, ComputeClientCompositeOperations
from oci.core.models.instance import Instance
from oci.response import Response

from oci_emulator import app
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

    def test_list_instances_without_params(self):
        response: Response = self.compute_cli.list_instances(
            self.oci_config["compartment_id"]
        )

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_list_instances_with_params(self):
        response: Response = self.compute_cli.list_instances(
            self.oci_config["compartment_id"], display_name="dummy-instance"
        )

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

        instances: List[Instance] = response.data
        test_instance = instances[0]

        self.assertEqual(test_instance.display_name, self.test_instance.display_name)

        response: Response = self.compute_cli.list_instances(
            self.oci_config["compartment_id"], display_name="oopsss"
        )

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)

    def tearDown(self):
        terminate_instance(self.test_instance.id, self.compute_cli)
        self.server.shutdown()
