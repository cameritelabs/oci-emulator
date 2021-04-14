from unicodedata import name
import unittest

import requests
import oci

from oci_emulator import app
from . import get_oci_config, ServerThread


def create_file(cli, namespace_name, bucket_name, file_name, content):
    r = cli.put_object(
        namespace_name=namespace_name,
        bucket_name=bucket_name,
        object_name=file_name,
        put_object_body=content,
        content_type="text/plain",
        cache_control="private, Immutable, max-age=31557600",
    )


def delete_file(cli, namespace_name, bucket_name, file_name):
    cli.delete_object(
        namespace_name=namespace_name, bucket_name=bucket_name, object_name=file_name
    )


class BucketRoutes(unittest.TestCase):
    def setUp(self):
        self.server = ServerThread(app)
        self.server.start()
        self.oci_config = get_oci_config()

    def test_no_auth(self):
        r = requests.get("http://localhost:12000/n/namespace/b")
        self.assertEqual(r.status_code, 404)
        r = requests.post("http://localhost:12000/n/namespace/b")
        self.assertEqual(r.status_code, 404)
        r = requests.delete("http://localhost:12000/n/namespace/b/bucket_name")
        self.assertEqual(r.status_code, 404)

    def test_bucket_route(self):
        cli = oci.object_storage.ObjectStorageClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        r = cli.get_namespace()
        namespace_name = r.data

        create_opts = oci.object_storage.models.CreateBucketDetails(
            name="bucket_name",
            compartment_id="compartment_id",
            public_access_type="ObjectRead",
            storage_tier="Standard",
            freeform_tags={"tag_name": "tag_value"},
            versioning="Disabled",
        )

        r = cli.create_bucket(
            namespace_name=namespace_name, create_bucket_details=create_opts
        )
        self.assertEqual(r.status, 200)

        r = cli.list_buckets(
            namespace_name=namespace_name, compartment_id="compartment_id"
        )
        self.assertEqual(r.status, 200)
        self.assertEqual(len(r.data), 1)

        r = cli.delete_bucket(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 204)
        r = cli.list_buckets(
            namespace_name=namespace_name, compartment_id="compartment_id"
        )
        self.assertEqual(r.status, 200)
        self.assertEqual(len(r.data), 0)

    def test_bucket_and_object(self):
        cli = oci.object_storage.ObjectStorageClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        r = cli.get_namespace()
        namespace_name = r.data

        create_opts = oci.object_storage.models.CreateBucketDetails(
            name="bucket_name",
            compartment_id="compartment_id",
            public_access_type="ObjectRead",
            storage_tier="Standard",
            freeform_tags={"tag_name": "tag_value"},
            versioning="Disabled",
        )

        r = cli.create_bucket(
            namespace_name=namespace_name, create_bucket_details=create_opts
        )
        self.assertEqual(r.status, 200)

        r = cli.put_object(
            namespace_name=namespace_name,
            bucket_name="bucket_name",
            object_name="folder/file.txt",
            put_object_body=b"teste alo testando",
            content_type="text/plain",
            cache_control="private, Immutable, max-age=31557600",
        )

        self.assertEqual(r.status, 200)

        r = cli.list_objects(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 200)
        r.data: oci.object_storage.models.list_objects.ListObjects

        self.assertEqual(len(r.data.objects), 1)

        r = requests.get(
            "http://localhost:12000/n/namespace_name/b/bucket_name/o/folder/file.txt"
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "teste alo testando")

        r = cli.delete_object(
            namespace_name=namespace_name,
            bucket_name="bucket_name",
            object_name="folder/file.txt",
        )

        r = cli.list_objects(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 200)
        r.data: oci.object_storage.models.list_objects.ListObjects

        self.assertEqual(len(r.data.objects), 0)

        r = cli.delete_bucket(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 204)

    def test_object_with_filter(self):
        cli = oci.object_storage.ObjectStorageClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        r = cli.get_namespace()
        namespace_name = r.data

        create_opts = oci.object_storage.models.CreateBucketDetails(
            name="bucket_name",
            compartment_id="compartment_id",
            public_access_type="ObjectRead",
            storage_tier="Standard",
            freeform_tags={"tag_name": "tag_value"},
            versioning="Disabled",
        )

        r = cli.create_bucket(
            namespace_name=namespace_name, create_bucket_details=create_opts
        )
        self.assertEqual(r.status, 200)

        create_file(cli, namespace_name, "bucket_name", "folder/fileOne", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/fileTwo", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/fileThree", b"teste")
        create_file(
            cli, namespace_name, "bucket_name", "Anotherfolder/fileOne", b"teste"
        )

        r = cli.list_objects(
            namespace_name=namespace_name, bucket_name="bucket_name", prefix="folder"
        )
        self.assertEqual(r.status, 200)

        self.assertEqual(len(r.data.objects), 3)

        delete_file(cli, namespace_name, "bucket_name", "folder/fileOne")
        delete_file(cli, namespace_name, "bucket_name", "folder/fileTwo")
        delete_file(cli, namespace_name, "bucket_name", "folder/fileThree")
        delete_file(cli, namespace_name, "bucket_name", "Anotherfolder/fileOne")

        r = cli.delete_bucket(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 204)

    def test_object_with_start(self):
        cli = oci.object_storage.ObjectStorageClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        r = cli.get_namespace()
        namespace_name = r.data

        create_opts = oci.object_storage.models.CreateBucketDetails(
            name="bucket_name",
            compartment_id="compartment_id",
            public_access_type="ObjectRead",
            storage_tier="Standard",
            freeform_tags={"tag_name": "tag_value"},
            versioning="Disabled",
        )

        r = cli.create_bucket(
            namespace_name=namespace_name, create_bucket_details=create_opts
        )
        self.assertEqual(r.status, 200)

        create_file(cli, namespace_name, "bucket_name", "folder/1", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/2", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/3", b"teste")

        r = cli.list_objects(
            namespace_name=namespace_name, bucket_name="bucket_name", start="folder/2"
        )
        self.assertEqual(r.status, 200)

        self.assertEqual(len(r.data.objects), 2)

        delete_file(cli, namespace_name, "bucket_name", "folder/1")
        delete_file(cli, namespace_name, "bucket_name", "folder/2")
        delete_file(cli, namespace_name, "bucket_name", "folder/3")

        r = cli.delete_bucket(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 204)

    def test_object_with_end(self):
        cli = oci.object_storage.ObjectStorageClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        r = cli.get_namespace()
        namespace_name = r.data

        create_opts = oci.object_storage.models.CreateBucketDetails(
            name="bucket_name",
            compartment_id="compartment_id",
            public_access_type="ObjectRead",
            storage_tier="Standard",
            freeform_tags={"tag_name": "tag_value"},
            versioning="Disabled",
        )

        r = cli.create_bucket(
            namespace_name=namespace_name, create_bucket_details=create_opts
        )
        self.assertEqual(r.status, 200)

        create_file(cli, namespace_name, "bucket_name", "folder/1", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/2", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/3", b"teste")

        r = cli.list_objects(
            namespace_name=namespace_name, bucket_name="bucket_name", end="folder/1"
        )
        self.assertEqual(r.status, 200)

        self.assertEqual(len(r.data.objects), 1)

        delete_file(cli, namespace_name, "bucket_name", "folder/1")
        delete_file(cli, namespace_name, "bucket_name", "folder/2")
        delete_file(cli, namespace_name, "bucket_name", "folder/3")

        r = cli.delete_bucket(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 204)

    def test_object_with_delimiter(self):
        cli = oci.object_storage.ObjectStorageClient(
            self.oci_config["config"], service_endpoint="http://localhost:12000"
        )

        r = cli.get_namespace()
        namespace_name = r.data

        create_opts = oci.object_storage.models.CreateBucketDetails(
            name="bucket_name",
            compartment_id="compartment_id",
            public_access_type="ObjectRead",
            storage_tier="Standard",
            freeform_tags={"tag_name": "tag_value"},
            versioning="Disabled",
        )

        r = cli.create_bucket(
            namespace_name=namespace_name, create_bucket_details=create_opts
        )
        self.assertEqual(r.status, 200)

        create_file(cli, namespace_name, "bucket_name", "folder/1", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/2", b"teste")
        create_file(cli, namespace_name, "bucket_name", "folder/3", b"teste")
        create_file(cli, namespace_name, "bucket_name", "otherFolder/1", b"teste")
        create_file(cli, namespace_name, "bucket_name", "notAFolder", b"teste")

        r = cli.list_objects(
            namespace_name=namespace_name, bucket_name="bucket_name", delimiter="/"
        )
        self.assertEqual(r.status, 200)

        self.assertEqual(len(r.data.objects), 1)
        self.assertEqual(r.data.objects[0].name, "notAFolder")
        self.assertEqual(r.data.prefixes, ["folder/", "otherFolder/"])

        delete_file(cli, namespace_name, "bucket_name", "folder/1")
        delete_file(cli, namespace_name, "bucket_name", "folder/2")
        delete_file(cli, namespace_name, "bucket_name", "folder/3")
        delete_file(cli, namespace_name, "bucket_name", "otherFolder/1")
        delete_file(cli, namespace_name, "bucket_name", "notAFolder")

        r = cli.delete_bucket(namespace_name=namespace_name, bucket_name="bucket_name")
        self.assertEqual(r.status, 204)

    def tearDown(self):
        self.server.shutdown()
