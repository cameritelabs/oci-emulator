import unittest
from threading import Thread

import requests
from werkzeug.serving import make_server

from oci_emulator import app


class ServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.srv = make_server("127.0.0.1", 12000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


class SampleRoutes(unittest.TestCase):
    def setUp(self):
        self.server = ServerThread(app)
        self.server.start()

    def test_sample_route(self):
        r = requests.get("http://localhost:12000")
        self.assertEqual(r.status_code, 200)

    def tearDown(self):
        self.server.shutdown()
