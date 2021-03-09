import logging
import json

from flask import Blueprint
from flask import request, Response

from app.resources.object_storage.buckets import (
    create_bucket,
    list_buckets,
    remove_bucket,
)

logger = logging.getLogger(__name__)
bucket_operations = Blueprint("bucket_operations", __name__)


@bucket_operations.route("/n/<namespace_name>/b", methods=["POST"])
def post_bucket(namespace_name):

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
    tenancy, user, fingerprint = None, None, None
    headers = request.headers["Authorization"].split(",")

    for header in headers:
        if "keyId=" in header:
            header = header.replace('keyId="', "").replace('"', "")
            tenancy, user, fingerprint = header.split("/")

    success, response = create_bucket(
        namespace=namespace_name, userId=user, bucket=json.loads(request.data)
    )

    if not success:
        bucket_name = json.loads(request.data)["name"]
        return Response(
            status=409,
            response=json.dumps(
                {
                    "code": "BucketAlreadyExists",
                    "message": f"Either the bucket '{bucket_name}' in namespace '{namespace_name}' already exists or you are not authorized to create it",
                }
            ),
            content_type="application/json",
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    return Response(
        status=200,
        response=json.dumps(response),
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@bucket_operations.route("/n/<namespace_name>/b", methods=["GET"])
def get_buckets(namespace_name):

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

    return Response(
        status=200,
        response=json.dumps(
            list_buckets(
                namespace=namespace_name, compartment_id=request.args["compartmentId"]
            )
        ),
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@bucket_operations.route("/n/<namespace_name>/b/<bucket_name>", methods=["DELETE"])
def delete_buckets(namespace_name, bucket_name):

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

    success, err = remove_bucket(namespace=namespace_name, bucket_name=bucket_name)
    if not success:
        if err == "not_found":
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
        elif err == "has_objects":
            return Response(
                status=409,
                content_type="application/json",
                response=json.dumps(
                    {
                        "code": "BucketNotEmpty",
                        "message": f"Bucket named '{bucket_name}' is not empty. Delete all object versions first.",
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
