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
    }
}

service_endpoint = None  # Use it to test on a real environment
# service_endpoint = "http://localhost:12000"  # Use it to test on mock environment
compartment_id = os.getenv("COMPARTMENT_ID")

cli = oci.object_storage.ObjectStorageClient(
    oci_config["config"], service_endpoint=service_endpoint
)
r = cli.get_namespace()
namespace_name = r.data


def monitoring():
    cli = oci.monitoring.MonitoringClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    # list_metrics_details = oci.monitoring.models.ListMetricsDetails(
    #     # name="resourceDisplayName"
    #     namespace="oci_objectstorage",
    #     dimension_filters={"resourceDisplayName": "architectureevents"},
    # )

    # b = cli.list_metrics(
    #     compartment_id=compartment_id, list_metrics_details=list_metrics_details
    # )

    summarize_metrics_data_details = oci.monitoring.models.SummarizeMetricsDataDetails(
        namespace="oci_objectstorage", query="StoredBytes[1h].mean()"
    )

    b = cli.summarize_metrics_data(
        compartment_id=compartment_id,
        summarize_metrics_data_details=summarize_metrics_data_details,
    )
    # cli.summarize_metrics_data(compartment_id=compartment_id, )
    # print(b.request_id)
    # print(b.headers)
    # print(b.data)
    # print(b.status)

    for item in b.data:
        print(
            item.dimensions["resourceDisplayName"],
            int(item.aggregated_datapoints[-1].value),
            from_byte_to_x(int(item.aggregated_datapoints[-1].value)),
        )

    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    b = cli.get_bucket(
        namespace_name=namespace_name,
        bucket_name="architectureevents",
        fields=["approximateCount", "approximateSize"],
    )

    # print(b.request_id)
    # print(b.headers)
    print(b.data.approximate_size)
    # print(b.status)


def from_byte_to_x(value):
    if value < 1024:
        return f"{value}B"

    value = value / 1024

    if value < 1024:
        return f"{value}KB"

    value = value / 1024

    if value < 1024:
        return f"{value}MB"

    value = value / 1024

    if value < 1024:
        return f"{value}GB"

    value = value / 1024

    if value < 1024:
        return f"{value}TB"

    value = value / 1024

    if value < 1024:
        return f"{value}PB"

    value = value / 1024


def list_buckets():

    cli = oci.object_storage.ObjectStorageClient(
        oci_config["config"], service_endpoint=service_endpoint
    )

    b = cli.list_buckets(namespace_name=namespace_name, compartment_id=compartment_id)

    b = cli.get_bucket(
        namespace_name=namespace_name,
        bucket_name="architectureevents",
        fields=["approximateCount", "approximateSize"],
    )

    # b = cli.head_bucket(namespace_name=namespace_name, bucket_name="architectureevents")

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

    print(r.request_id)
    print(r.headers)
    print(r.data)
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


def create_table():

    ddl_statement = """
    CREATE TABLE table_name ( campo1 string, campo2 number, campo3 string DEFAULT "[]" NOT NULL, PRIMARY KEY ( SHARD ( campo1 ), campo2 ) )
    """

    table_limits = oci.nosql.models.TableLimits(
        max_read_units=1, max_write_units=1, max_storage_in_g_bs=1
    )

    nosql_details = oci.nosql.models.CreateTableDetails(
        name="table_name",
        compartment_id=compartment_id,
        ddl_statement=ddl_statement,
        table_limits=table_limits,
    )

    cli = oci.nosql.NosqlClient(oci_config["config"], service_endpoint=service_endpoint)
    r = cli.create_table(create_table_details=nosql_details)

    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


def create_row():
    nosql_row = oci.nosql.models.UpdateRowDetails()
    nosql_row.value = {"campo1": "value1", "campo2": 1}
    nosql_row.compartment_id = compartment_id

    cli = oci.nosql.NosqlClient(oci_config["config"], service_endpoint=service_endpoint)

    r = cli.update_row(table_name_or_id="table_name", update_row_details=nosql_row)

    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


def query():
    cli = oci.nosql.NosqlClient(oci_config["config"], service_endpoint=service_endpoint)

    q = f"SELECT * FROM table_name"
    details = oci.nosql.models.QueryDetails(compartment_id=compartment_id, statement=q)

    r = cli.query(details)

    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


def delete_row():
    cli = oci.nosql.NosqlClient(oci_config["config"], service_endpoint=service_endpoint)
    r = cli.delete_row(
        table_name_or_id="table_name",
        compartment_id=compartment_id,
        key=[f"campo1:value1", f"campo2:1"],
    )
    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


def delete_table():
    cli = oci.nosql.NosqlClient(oci_config["config"], service_endpoint=service_endpoint)
    r = cli.delete_table(table_name_or_id="table_name", compartment_id=compartment_id)
    print(r.request_id)
    print(r.headers)
    print(r.data)
    print(r.status)


a = monitoring()

# create_bucket()
# put_object()
# create_table()
# create_row()
# query()
# delete_row()
# delete_table()
