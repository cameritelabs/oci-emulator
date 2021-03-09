import logging
import json

from flask import Blueprint
from flask import request, Response

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

    if False:
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

    return ""


@objects.route("/n/<namespace_name>/b/<bucket_name>/o", methods=["GET"])
def get_objects(namespace_name, bucket_name):
    return ""


@objects.route("/n/<namespace_name>/b/<bucket_name>/o/<path:subpath>", methods=["GET"])
def get_object(namespace_name, bucket_name, subpath):

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
                    "message": f"The object '{subpath}' was not found in the bucket '{bucket_name}'",
                }
            ),
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
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

