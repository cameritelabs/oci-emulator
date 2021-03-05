import oci

oci_config = {
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


def compute_client_sample():

    cli = oci.core.ComputeClient(
        oci_config["config"], service_endpoint="http://localhost:12000"
    )

    cli.list_instances("compartment_id")


def object_storage_sample():

    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint="http://localhost:12000"
    )

    create_opts = oci.object_storage.models.CreateBucketDetails(
        name="bucket_name",
        compartment_id="compartment_id",
        public_access_type="ObjectRead",
        storage_tier="Standard",
        freeform_tags={"tag_name": "tag_value"},
        versioning="Disabled",
    )

    cli.create_bucket(
        namespace_name="namespace_name", create_bucket_details=create_opts
    )
