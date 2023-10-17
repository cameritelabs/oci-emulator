import logging
import json

from flask import Blueprint
from flask import request, Response

from app.resources.queues.queues import add_queue, delete_queue, get_queue_by_id, list_queues


logger = logging.getLogger(__name__)
queues = Blueprint("queues", __name__)

@queues.route("/<date>/queues", methods=["POST"])
def post_queues(date: str):

    data = json.loads(request.data)
    add_queue(data)

    return Response(
        status=200,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )

@queues.route("/<date>/queues", methods=["GET"])
def get_list_queues(date: str):

    response = {
        "items": list_queues(compartment_id=request.args["compartmentId"]),
    }

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

@queues.route("/<date>/queues/<queue_id>", methods=["GET"])
def get_queues(date: str, queue_id: str):

    response = get_queue_by_id(queue_id)

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

@queues.route("/<date>/queues/<queue_id>", methods=["DELETE"])
def delete_queues(date: str, queue_id: str):

    success, err = delete_queue(queue_id)

    if not success:
        if err == "not_found":
            return Response(
                status=404,
                content_type="application/json",
                headers={
                    "opc-request-id": request.headers["Opc-Request-Id"]
                    if "Opc-Request-Id" in request.headers
                    else ""
                },
            )

    return Response(
        status=200,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )
