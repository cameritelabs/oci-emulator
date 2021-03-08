import dotenv
import oci
import os

dotenv.load_dotenv()

oci_config = {
    "config": {
        "user": os.getenv("OCI_USER"),
        "fingerprint": os.getenv("OCI_FINGERPRINT"),
        "tenancy": os.getenv("OCI_TENANCY"),
        "region": os.getenv("OCI_REGION"),
        "key_file": os.getenv("OCI_KEY_FILE"),
        "pass_phrase": os.getenv("OCI_PASS_PHRASE"),
    }
}

# service_endpoint = None  # Use it to test on a real environment
service_endpoint = "http://localhost:12000"  # Use it to test on mock environment


def list_buckets():
    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    b = cli.list_buckets(
        namespace_name="namespace_name", compartment_id="compartment_id"
    )

    print(b.request_id)
    print(b.headers)
    print(b.data)
    print(b.status)


def compute_client_sample():

    cli = oci.core.ComputeClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    cli.list_instances("compartment_id")


def create_bucket():

    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    create_opts = oci.object_storage.models.CreateBucketDetails(
        name="bucket_name",
        compartment_id="compartment_id",
        public_access_type="ObjectRead",
        storage_tier="Standard",
        freeform_tags={"tag_name": "tag_value"},
        versioning="Disabled",
    )

    a = cli.create_bucket(
        namespace_name="namespace_name", create_bucket_details=create_opts
    )
    print(a.request_id)
    print(a.headers)
    print(a.data)
    print(a.status)


create_bucket()
list_buckets()
