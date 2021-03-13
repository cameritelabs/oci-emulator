from unittest import TestCase
from time import sleep

from oci.core import ComputeClient, ComputeClientCompositeOperations
from oci.response import Response
from oci.exceptions import ServiceError

from oci_emulator import app
from tests import get_oci_config, ServerThread
from tests.compute import create_instance


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

    def test_terminate_instance(self):
        response: Response = self.compute_cli.terminate_instance(self.test_instance.id)
        self.assertEqual(response.status, 204)

        sleep(5)

        with self.assertRaises(ServiceError) as e:
            self.compute_cli.get_instance(self.test_instance.id)
            self.assertEqual(e.exception.status, 404)

    def test_terminate_non_existent_instance(self):
        with self.assertRaises(ServiceError) as e:
            self.compute_cli.get_instance("non_existent_instance")
            self.assertEqual(e.exception.status, 404)

    def tearDown(self):
        self.server.shutdown()
