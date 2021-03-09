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
namespace_name = os.getenv("NAMESPACE_NAME")
compartment_id = os.getenv("COMPARTMENT_ID")


def list_buckets():
    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    b = cli.list_buckets(namespace_name=namespace_name, compartment_id=compartment_id)

    print(b.request_id)
    print(b.headers)
    print(b.data)
    print(b.status)


def compute_client_sample():

    cli = oci.core.ComputeClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    cli.list_instances(compartment_id)


def create_bucket():

    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    create_opts = oci.object_storage.models.CreateBucketDetails(
        name="bucket_name",
        compartment_id=compartment_id,
        public_access_type="ObjectRead",
        storage_tier="Standard",
        freeform_tags={"tag_name": "tag_value"},
        versioning="Disabled",
    )

    a = cli.create_bucket(
        namespace_name=namespace_name, create_bucket_details=create_opts
    )
    print(a.request_id)
    print(a.headers)
    print(a.data)
    print(a.status)


def delete_bucket():
    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    r = cli.delete_bucket(namespace_name=namespace_name, bucket_name="bucket_name")
    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


def put_object():
    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )
    r = cli.put_object(
        namespace_name=namespace_name,
        bucket_name="bucket_name",
        object_name="folder/file.txt",
        put_object_body=b"teste alo testando",
        content_type="text/plain",
        cache_control="private, Immutable, max-age=31557600",
    )

    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


def list_objects():
    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )
    r = cli.list_objects(namespace_name=namespace_name, bucket_name="bucket_name")
    # {"objects":[{"name":"folder/file.txt"}]}

    print(r.request_id)
    print(r.headers)
    print(r.data)
    # {
    #     "next_start_with": null,
    #     "objects": [
    #         {
    #             "archival_state": null,
    #             "etag": null,
    #             "md5": null,
    #             "name": "folder/file.txt",
    #             "size": null,
    #             "storage_tier": null,
    #             "time_created": null,
    #             "time_modified": null,
    #         }
    #     ],
    #     "prefixes": null,
    # }
    print(r.status)


def delete_object():
    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )
    r = cli.delete_object(
        namespace_name=namespace_name,
        bucket_name="bucket_name",
        object_name="folder/file.txt",
    )

    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


# create_bucket()
# list_buckets()
# delete_bucket()
put_object()
# list_objects()
# delete_object()
