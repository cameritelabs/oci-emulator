import unittest
from threading import Thread
import requests

import oci
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


class BucketRoutes(unittest.TestCase):
    def setUp(self):
        self.server = ServerThread(app)
        self.server.start()

        self.oci_config = {
            "config": {
                "user": "ocid1.user.oc1..random",
                "fingerprint": "50:a6:c1:a1:da:71:57:dc:87:ae:90:af:9c:38:99:67",
                "tenancy": "ocid1.tenancy.oc1..random",
                "region": "sa-saopaulo-1",
                "key_file": "assets/keys/private_key.pem",
                "pass_phrase": "",
            },
            "test_compartment_id": "ocid1.compartment.oc1..randomcompartment",
        }

    def test_no_auth(self):
        r = requests.get("http://localhost:12000/n/namespace/b")
        self.assertEqual(r.status_code, 404)
        r = requests.post("http://localhost:12000/n/namespace/b")
        self.assertEqual(r.status_code, 404)
        r = requests.delete("http://localhost:12000/n/namespace/b/bucket_name")
        self.assertEqual(r.status_code, 404)

    def test_sample_route(self):
        cli = oci.object_storage.ObjectStorageClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        create_opts = oci.object_storage.models.CreateBucketDetails(
            name="bucket_name",
            compartment_id="compartment_id",
            public_access_type="ObjectRead",
            storage_tier="Standard",
            freeform_tags={"tag_name": "tag_value"},
            versioning="Disabled",
        )

        r = cli.create_bucket(
            namespace_name="namespace_name", create_bucket_details=create_opts
        )
        self.assertEqual(r.status, 200)

        r = cli.list_buckets(
            namespace_name="namespace_name", compartment_id="compartment_id"
        )
        self.assertEqual(r.status, 200)
        self.assertEqual(len(r.data), 1)

        r = cli.delete_bucket(
            namespace_name="namespace_name", bucket_name="bucket_name"
        )
        self.assertEqual(r.status, 204)
        r = cli.list_buckets(
            namespace_name="namespace_name", compartment_id="compartment_id"
        )
        self.assertEqual(r.status, 200)
        self.assertEqual(len(r.data), 0)

    def tearDown(self):
        self.server.shutdown()
