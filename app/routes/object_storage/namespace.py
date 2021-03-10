import logging
import json
import uuid
import os

from flask import Blueprint
from flask import request, Response

logger = logging.getLogger(__name__)
namespace = Blueprint("namespace", __name__)


@namespace.route("/n", methods=["GET"])
def get_namespace():
    return Response(
        status=200,
        content_type="application/json",
        response="namespace_name",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )
