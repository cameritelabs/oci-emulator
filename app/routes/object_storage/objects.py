import logging
import json
import uuid
import os
import time
from email.utils import formatdate

from flask import Blueprint
from flask import request, Response

from app.resources.object_storage.buckets import get_bucket, get_object
from app.resources.object_storage.objects import get_objects

logger = logging.getLogger(__name__)
objects = Blueprint("objects", __name__)


@objects.route("/n/<namespace_name>/b/<bucket_name>/o/<path:subpath>", methods=["HEAD"])
def head_object(namespace_name, bucket_name, subpath):
    bucket = get_bucket(namespace=namespace_name, bucket_name=bucket_name)
    if bucket is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "BucketNotFound",
                    "message": f"Either the bucket named '{bucket_name}' does not exist in the namespace '{namespace_name}' or you are not authorized to access it",
                }
            ),
            headers={"opc-request-id": request.headers.get("Opc-Request-Id", "")},
        )

    _object = get_object(bucket=bucket, object_name=subpath)
    if _object is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "ObjectNotFound",
                    "message": f"The object '{subpath}' was not found in the bucket '{bucket_name}'",
                }
            ),
            headers={"opc-request-id": request.headers.get("Opc-Request-Id", "")},
        )

    etag = _object.get("etag", str(uuid.uuid4()))
    content_type = _object.get("content_type", "application/octet-stream")
    content_length = _object.get("size", 0)
    content_encoding = _object.get("content_encoding", "")
    cache_control = _object.get("cache_control", "")
    content_disposition = _object.get("content_disposition", "")
    last_modified_ts = _object.get("last_modified", time.time())
    last_modified_str = formatdate(last_modified_ts, True)
    opc_meta = _object.get("opc_meta", {})
    opc_content_crc32c = _object.get("opc-content-crc32c", "")

    return Response(
        status=200,
        # No body for HEAD: we only send headers
        headers={
            "etag": etag,
            "Content-Type": content_type,
            "Content-Length": str(content_length),
            "Content-Encoding": content_encoding,
            "opc-request-id": request.headers.get("Opc-Request-Id", ""),
            "LastModified": last_modified_str,
            "Cache-Control": cache_control,
            "Content-Disposition": content_disposition,
            "opc-meta": opc_meta,
            "opc-content-crc32c": opc_content_crc32c,
        },
    )


@objects.route("/n/<namespace_name>/b/<bucket_name>/o/<path:subpath>", methods=["PUT"])
def put_object(namespace_name, bucket_name, subpath):
    cache_control = None
    content_type = None
    content_disposition = None
    content_encoding = None
    metadata = None

    if "Cache-Control" in request.headers:
        cache_control = request.headers["Cache-Control"]

    if "Content-Type" in request.headers:
        content_type = request.headers["Content-Type"]

    if "Content-Encoding" in request.headers:
        content_encoding = request.headers["Content-Encoding"]

    if "Content-Disposition" in request.headers:
        content_disposition = request.headers["Content-Disposition"]

    if "opc-meta" in request.headers:
        metadata = request.headers["opc-meta"]

    bucket = get_bucket(namespace=namespace_name, bucket_name=bucket_name)

    if bucket is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "BucketNotFound",
                    "message": f"Either the bucket named '{bucket_name}' does not exist in the namespace '{namespace_name}' or you are not authorized to access it",
                }
            ),
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    ref_obj = str(uuid.uuid4())
    with open(f"tmp/{ref_obj}", "wb") as file:
        file.write(request.data)

    last_modified = time.time()
    opc_content_crc32c = "opc-content-crc32c"
    bucket["_objects"].append(
        {
            "cache_control": cache_control,
            "content_type": content_type,
            "content_encoding": content_encoding,
            "object_name": subpath,
            "ref_obj": ref_obj,
            "content_disposition": content_disposition,
            "etag": str(uuid.uuid4()),
            "size": len(request.data),
            "last_modified": last_modified,
            "opc_meta": metadata,
            "opc-content-crc32c": opc_content_crc32c,
        }
    )

    return Response(
        status=200,
        headers={
            "etag": bucket["_objects"][-1]["etag"],
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else "",
        },
    )


@objects.route("/n/<namespace_name>/b/<bucket_name>/o", methods=["GET"])
def list_objects(namespace_name, bucket_name):

    prefix = request.args.get("prefix")
    start = request.args.get("start")
    delimiter = request.args.get("delimiter")
    end = request.args.get("end")

    kwargs = {}
    if prefix is not None:
        kwargs["prefix"] = prefix
    if start is not None:
        kwargs["start"] = start
    if end is not None:
        kwargs["end"] = end
    if delimiter is not None:
        kwargs["delimiter"] = delimiter

    bucket = get_bucket(namespace=namespace_name, bucket_name=bucket_name)
    if bucket is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "BucketNotFound",
                    "message": f"Either the bucket named '{bucket_name}' does not exist in the namespace '{namespace_name}' or you are not authorized to access it",
                }
            ),
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    objects = []
    prefixes = []
    if len(bucket["_objects"]):
        objects, prefixes = get_objects(bucket, **kwargs)

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps({"objects": objects, "prefixes": prefixes}),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@objects.route("/n/<namespace_name>/b/<bucket_name>/o/<path:subpath>", methods=["GET"])
def get_object_route(namespace_name, bucket_name, subpath):

    bucket = get_bucket(namespace=namespace_name, bucket_name=bucket_name)
    if bucket is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "BucketNotFound",
                    "message": f"Either the bucket named '{bucket_name}' does not exist in the namespace '{namespace_name}' or you are not authorized to access it",
                }
            ),
            headers={},
        )

    _object = get_object(bucket=bucket, object_name=subpath)
    if _object is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "ObjectNotFound",
                    "message": f"The object '{subpath}' was not found in the bucket '{bucket_name}'",
                }
            ),
            headers={},
        )

    file = open(f"tmp/{_object['ref_obj']}", "rb")
    content = file.read()
    file.close()

    return Response(
        status=200,
        content_type=_object["content_type"],
        response=content,
        headers={
            "etag": _object["etag"],
            "Cache-Control": _object["cache_control"],
            "Content-Disposition": _object["content_disposition"],
        },
    )


@objects.route(
    "/n/<namespace_name>/b/<bucket_name>/o/<path:subpath>", methods=["DELETE"]
)
def delete_object(namespace_name, bucket_name, subpath):

    bucket = get_bucket(namespace=namespace_name, bucket_name=bucket_name)
    if bucket is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "BucketNotFound",
                    "message": f"Either the bucket named '{bucket_name}' does not exist in the namespace '{namespace_name}' or you are not authorized to access it",
                }
            ),
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    _object = get_object(bucket=bucket, object_name=subpath)
    if _object is None:
        return Response(
            status=404,
            content_type="application/json",
            response=json.dumps(
                {
                    "code": "ObjectNotFound",
                    "message": f"The object '{subpath}' does not exist in bucket '{bucket_name}' with namespace '{namespace_name}'",
                }
            ),
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    bucket["_objects"].remove(_object)
    os.remove(f"tmp/{_object['ref_obj']}")

    return Response(
        status=204,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )
