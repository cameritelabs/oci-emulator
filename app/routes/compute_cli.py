import logging
import json

from flask import Blueprint, request, Response

from app.resources.compute import (
    create_instance,
    get_instances,
    find_instance,
    terminate_instance,
)

logger = logging.getLogger(__name__)
compute = Blueprint("compute", __name__)


def bad_request(field: str):
    return Response(f"{field} is required!", status=400)


@compute.route("/instances", methods=["POST"])
def launch_instance():
    data = request.json

    if "availabilityDomain" not in data:  # "utiT:SA-SAOPAULO-1-AD-1"
        return bad_request("availabilityDomain")

    if "compartmentId" not in data:
        return bad_request("compartmentId")

    if "shape" not in data:
        return bad_request("shape")

    instance = create_instance(
        data["availabilityDomain"],
        data["compartmentId"],
        data["shape"],
        displayName=data["displayName"] if "displayName" in data else None,
    )

    return Response(
        status=200, content_type="application/json", response=json.dumps(instance)
    )


@compute.route("/instances", methods=["GET"])
def list_instances():
    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(get_instances()),
    )


@compute.route("/instances/<instance_ocid>", methods=["GET"])
def get_instance(instance_ocid):
    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(find_instance(instance_ocid)),
    )


@compute.route("/instances/<instance_ocid>", methods=["DELETE"])
def delete_instance(instance_ocid):
    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(terminate_instance(instance_ocid)),
    )
