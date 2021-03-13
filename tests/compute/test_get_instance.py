from typing import List
from unittest import TestCase

from oci.core import ComputeClient, ComputeClientCompositeOperations
from oci.core.models.instance import Instance
from oci.response import Response
from oci.exceptions import ServiceError

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

    def test_get_instance(self):
        response: Response = self.compute_cli.list_instances(
            self.oci_config["compartment_id"], display_name="dummy-instance"
        )
        instances: List[Instance] = response.data
        test_instance = instances[0]

        response: Response = self.compute_cli.get_instance(test_instance.id)

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.data, Instance)
        self.assertEqual(response.data.id, self.test_instance.id)

    def test_get_nonexistent_instance(self):
        with self.assertRaises(ServiceError) as e:
            self.compute_cli.get_instance("non_existent_instance")
            self.assertEqual(e.exception.status, 404)

    def tearDown(self):
        terminate_instance(self.test_instance.id, self.compute_cli)
        self.server.shutdown()
