import logging
import json

from flask import Blueprint
from flask import request, Response

from app.resources.nosql_database.tables import (
    add_table,
    find_table,
    remove_table,
    find_row,
    put_row_on_table,
    query_rows,
)

logger = logging.getLogger(__name__)
tables = Blueprint("tables", __name__)


@tables.route("/<date>/tables", methods=["POST"])
def post_table(date: str):
    add_table(json.loads(request.data))

    return Response(
        status=202,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@tables.route("/<date>/tables/<table_name>", methods=["DELETE"])
def delete_table(date: str, table_name: str):
    table = find_table(table_name, request.args.get("compartmentId", default=""))
    remove_table(table)

    return Response(
        status=202,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@tables.route("/<date>/tables/<table_name>", methods=["GET"])
def get_table(date: str, table_name: str):
    table = find_table(table_name, request.args.get("compartmentId", default=""))
    # The idea here is to maybe create a object will all this properties
    return Response(
        status=202,
        content_type="application/json",
        response=json.dumps(
            {
                "compartmentId": table["compartmentId"],
                "ddlStatement": table["ddlStatement"],
                "id": table["id"],
                "isAutoReclaimable": None,
                "lifecycleDetails": None,
                "lifecycleState": None,
                "name": table["name"],
                "schema": None,
                "tableLimits": table["tableLimits"],
                "timeCreated": None,
                "timeOfExpiration": None,
                "timeUpdated": None,
            }
        ),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@tables.route("/<date>/tables/<table_name>/rows", methods=["PUT"])
def put_row(date: str, table_name: str):
    data = json.loads(request.data)

    table = find_table(table_name, data.get("compartmentId", ""))
    put_row_on_table(table, data)

    return Response(
        status=200,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@tables.route("/<date>/query", methods=["POST"])
def query(date: str):
    data = json.loads(request.data)
    rows = query_rows(data["statement"], data["compartmentId"])

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps({"items": rows}),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@tables.route("/<date>/tables/<table_name>/rows", methods=["DELETE"])
def delete_row(date: str, table_name: str):
    table = find_table(table_name, request.args.get("compartmentId", default=""))

    keys = request.args.getlist("key")
    k = {}
    for key in keys:
        i = key.split(":")
        k[i[0]] = i[1]

    for row in table["_rows"]:
        found = True
        for key in k:
            if str(row[key]) != k[key] and str(row[key]) != k[key] + ".0":
                found = False

        if found:
            table["_rows"].remove(row)
            break

    return Response(
        status=200,
        content_type="application/json",
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@tables.route("/<date>/tables/<table_name>/rows", methods=["GET"])
def get_row(date: str, table_name: str):
    table = find_table(table_name, request.args.get("compartmentId", default=""))
    rows = table["_rows"]

    keys = request.args.getlist("key")
    k = {}
    for key in keys:
        i = key.split(":")
        k[i[0]] = i[1]

    row = find_row(rows, k)

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps({"value": row}),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )
