import logging

from os import environ
from threading import Thread
from typing import TypedDict

from werkzeug.serving import make_server

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

environ["USER"] = "ocid1.user.oc1..testuser"
environ["FINGERPRINT"] = "50:a6:c1:a1:da:71:57:dc:87:ae:90:af:9c:38:99:67"
environ["TENANCY"] = "ocid1.tenancy.oc1..testtenancy"
environ["REGION"] = "sa-saopaulo-1"
environ["KEY_FILE"] = "assets/keys/private_key.pem"
environ["COMPARTMENT_ID"] = "ocid1.compartment.oc1..testcompartment"


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


class Config(TypedDict):
    user: str
    fingerprint: str
    tenancy: str
    region: str
    key_file: str


class OciConfig(TypedDict):
    config: Config
    compartment_id: str


def get_oci_config() -> OciConfig:
    return {
        "config": {
            "user": environ["USER"],
            "fingerprint": environ["FINGERPRINT"],
            "tenancy": environ["TENANCY"],
            "region": environ["REGION"],
            "key_file": environ["KEY_FILE"],
        },
        "compartment_id": environ["COMPARTMENT_ID"],
    }
