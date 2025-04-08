import logging
import json

from flask import Blueprint
from flask import request, Response

from app.resources.queues.queues import (
    add_queue,
    delete_queue,
    get_queue_by_id,
    list_queues,
)


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
        "items": list_queues(
            compartment_id=request.args["compartmentId"],
            lifecycle_state=request.args["lifecycleState"]
            if "lifecycleState" in request.args
            else None,
        ),
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


@queues.route("/<date>/queues/<queue_id>/messages", methods=["POST"])
def post_messages(date: str, queue_id: str):
    data = json.loads(request.data)
    print(data)

    return Response(
        status=200,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
        response=json.dumps(
            {
                "messages": [
                    {
                        "id": 144115188077707275,
                        "expireAfter": "2023-09-28T12:51:33.522Z",
                    }
                ]
            }
        ),
    )


@queues.route("/<date>/queues/<queue_id>/messages", methods=["GET"])
def get_messages(date: str, queue_id: str):
    # data = json.loads(request.data)
    # print(data)

    return Response(
        status=200,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
        response=json.dumps(
            {
                "messages": [
                    {
                        "content": '{"name": "zéca" }',
                        "deliveryCount": 2,
                        "expireAfter": "2023-09-27T19:49:45.430000+00:00",
                        "id": 144115188077669364,
                        "metadata": None,
                        "receipt": "AVrHE2SlpkubAJiEgstJHDJr925mr4S-Fbw-n5yJTxAON-E7LEQOt1f6XHstKVIPv0h6yVnuPxxfDF3wq5jLBx_a5pkr0Uf9wAe15UzgbTvLGaSVzBHTmJtQTuYIunfxL8EaDzZzpVoHq4wzSPFQhY4y2NQ8UCi-gC4I4eerj8A0Ju2TIHM8w7GQpls-7aPSMfeC2WxZ44sDf72vDFveadSrm510W-NdfERWMjZohBvugdpZlfq0kxlOHhVm1zpznJslp1vUjpoi7NX4V_p5YbIV4-ZcUpypDhRAVIKYCCxhRhSJzcxIjwnsuHwfE-OXvv4nXXMkW3FPwo3DNhw0jIqnb7j9bmoQQ91khAU",
                        "visibleAfter": "2023-09-27T15:05:42.576000+00:00",
                    }
                ]
            }
        ),
    )
