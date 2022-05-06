import logging
import json

from threading import Thread
from functools import partial

from flask import Blueprint, request, Response

from app.resources.compute import (
    create_instance,
    get_instances,
    find_instance,
    terminate_instance,
    instance_action,
)
from app.enums.compute.instance_action import InstanceAction

logger = logging.getLogger(__name__)
compute = Blueprint("compute", __name__)


def bad_request(field: str, request):
    return Response(
        response=f"Unable to find {field} on request body!",
        status=400,
        content_type="text/plain",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@compute.route("/instances", methods=["POST"])
def launch_instance():
    data = request.json

    if "availabilityDomain" not in data:  # "utiT:SA-SAOPAULO-1-AD-1"
        return bad_request("availabilityDomain", request)

    if "compartmentId" not in data:
        return bad_request("compartmentId", request)

    if "shape" not in data:
        return bad_request("shape", request)

    instance = create_instance(
        data["availabilityDomain"],
        data["compartmentId"],
        data["shape"],
        display_name=data["displayName"] if "displayName" in data else None,
    )

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(instance),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@compute.route("/instances", methods=["GET"])
def list_instances():
    params = {"compartmentId": None, "displayName": None}

    compartment_id = request.args.get("compartmentId")
    display_name = request.args.get("displayName")

    if compartment_id:
        params["compartmentId"] = compartment_id

    if display_name:
        params["displayName"] = display_name

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(get_instances(params=params)),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@compute.route("/instances/<instance_ocid>", methods=["GET"])
def get_instance(instance_ocid):
    instance = find_instance(instance_ocid)

    if not instance:
        return Response(
            status=404,
            content_type="text/plain",
            response="Instance Not Found",
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(instance),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@compute.route("/instances/<instance_ocid>", methods=["DELETE"])
def delete_instance(instance_ocid):
    if not find_instance(instance_ocid):
        return Response(
            status=404,
            content_type="text/plain",
            response="Instance Not Found",
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    _terminate_instance = partial(terminate_instance, instance_ocid)
    Thread(target=_terminate_instance).start()

    return Response(
        status=204,
        content_type="text/plain",
        response="The instance is being terminated",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@compute.route("/instances/<instance_ocid>", methods=["POST"])
def perform_action(instance_ocid):
    instance = find_instance(instance_ocid)
    invalid_action_response = Response(
        response=f"Couldn't find action or it's value is invalid",
        status=400,
        content_type="text/plain",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )

    if not instance:
        return Response(
            status=404,
            content_type="text/plain",
            response="Instance Not Found",
            headers={
                "opc-request-id": request.headers["Opc-Request-Id"]
                if "Opc-Request-Id" in request.headers
                else ""
            },
        )

    if not request.args.get("action"):
        return invalid_action_response

    action: InstanceAction = InstanceAction.parse_str_to_enum(
        request.args.get("action")
    )

    if not action:
        return invalid_action_response

    instance_action(instance_ocid, action)

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(instance),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )
