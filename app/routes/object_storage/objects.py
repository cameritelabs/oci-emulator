import logging
import json
import uuid

from flask import Blueprint
from flask import request, Response

from app.resources.object_storage.buckets import get_bucket, get_object

logger = logging.getLogger(__name__)
objects = Blueprint("objects", __name__)


@objects.route("/n/<namespace_name>/b/<bucket_name>/o/<path:subpath>", methods=["PUT"])
def put_object(namespace_name, bucket_name, subpath):
    # TODO: this could probably become a middleware
    if "Authorization" not in request.headers:
        return Response(
            status=404,
            response=json.dumps(
                {
                    "code": "NotAuthorizedOrNotFound",
                    "message": "Authorization failed or requested resource not found.",
                }
            ),
            content_type="application/json",
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    cache_control = None
    content_type = None

    if "Cache-Control" in request.headers:
        cache_control = request.headers["Cache-Control"]

    if "Content-Type" in request.headers:
        content_type = request.headers["Content-Type"]

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

    bucket["_objects"].append(
        {
            "cache_control": cache_control,
            "content_type": content_type,
            "object_name": subpath,
            "ref_obj": ref_obj,
        }
    )

    return ""


@objects.route("/n/<namespace_name>/b/<bucket_name>/o", methods=["GET"])
def get_objects(namespace_name, bucket_name):
    return ""


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
        headers={"Cache-Control": _object["cache_control"]},
    )

    return ""


@objects.route(
    "/n/<namespace_name>/b/<bucket_name>/o/<path:subpath>", methods=["DELETE"]
)
def delete_object(namespace_name, bucket_name, subpath):

    # TODO: this could probably become a middleware
    if "Authorization" not in request.headers:
        return Response(
            status=404,
            response=json.dumps(
                {
                    "code": "NotAuthorizedOrNotFound",
                    "message": "Authorization failed or requested resource not found.",
                }
            ),
            content_type="application/json",
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    if False:
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

    return Response(
        status=204,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )

