from typing import List
import unittest

import oci

from oci_emulator import app
from . import get_oci_config, ServerThread


class IdentityRoutes(unittest.TestCase):
    def setUp(self) -> None:
        self.server = ServerThread(app)
        self.server.start()
        self.oci_config = get_oci_config()

        self.identity = oci.identity.IdentityClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

    def test_get_user(self):

        user: oci.identity.models.User = self.identity.get_user(
            self.oci_config["config"]["user"]
        ).data

        self.assertEquals(user.id, self.oci_config["config"]["user"])

    def test_list_users(self):

        users: List[oci.identity.models.User] = self.identity.list_users(
            self.oci_config["compartment_id"]
        ).data

        self.assertEquals(len(users), 1)
        self.assertEquals(users[0].compartment_id, self.oci_config["compartment_id"])

    def tearDown(self) -> None:
        self.server.shutdown()
