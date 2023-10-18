from unicodedata import name
import unittest

import oci

from oci_emulator import app
from . import get_oci_config, ServerThread


class QueuesRoutes(unittest.TestCase):
    def setUp(self):
        self.server = ServerThread(app)
        self.server.start()
        self.oci_config = get_oci_config()

    def test_bucket_route(self):
        cli = oci.queue.QueueAdminClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        create_queue_details = oci.queue.models.CreateQueueDetails(
            display_name="queue_test",
            compartment_id="compartment_id",
        )

        # create queue
        r = cli.create_queue(create_queue_details=create_queue_details)
        self.assertEqual(r.status, 200)

        # list queues
        r = cli.list_queues(compartment_id="compartment_id", lifecycle_state="ACTIVE")
        self.assertEqual(r.status, 200)
        self.assertEqual(len(r.data.items), 1)
        self.assertEqual(r.data.items[0].display_name, "queue_test")
        self.assertEqual(r.data.items[0].compartment_id, "compartment_id")

        # get queue
        r = cli.get_queue(queue_id=r.data.items[0].id)
        self.assertEqual(r.status, 200)
        self.assertEqual(r.data.display_name, "queue_test")
        self.assertEqual(r.data.compartment_id, "compartment_id")

        # delete queue
        r = cli.delete_queue(queue_id=r.data.id)
        self.assertEqual(r.status, 200)

    def tearDown(self):
        self.server.shutdown()
