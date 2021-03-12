import logging

from datetime import datetime

from flask import Blueprint, request, Response, jsonify

from app.resources.compute import create_instance, get_instances

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

    return instance


@compute.route("/instances", methods=["GET"])
def list_instances():
    return jsonify(get_instances())
