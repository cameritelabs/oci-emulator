import unittest

import requests

from oci_emulator import app
from . import ServerThread


class SampleRoutes(unittest.TestCase):
    def setUp(self):
        self.server = ServerThread(app)
        self.server.start()

    def test_sample_route(self):
        r = requests.get("http://localhost:12000")
        self.assertEqual(r.status_code, 404)

    def tearDown(self):
        self.server.shutdown()
