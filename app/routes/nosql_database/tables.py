import logging
import json

from flask import Blueprint
from flask import request, Response

from app.resources.nosql_database.tables import add_table, find_table, remove_table

logger = logging.getLogger(__name__)
tables = Blueprint("tables", __name__)


@tables.route("/<date>/tables", methods=["POST"])
def post_table(date):

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
def delete_table(date, table_name):

    table = find_table(table_name, request.args["compartmentId"])
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


@tables.route("/<date>/tables/<table_name>/rows", methods=["PUT"])
def put_row(date, table_name):

    data = json.loads(request.data)

    table = find_table(table_name, data["compartmentId"])
    table["_rows"].append(data["value"])

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
def query(date):

    data = json.loads(request.data)
    stmt = data["statement"].split(" ")

    table_name = ""
    for i in range(len(stmt)):
        if stmt[i] == "FROM":
            table_name = stmt[i + 1]
            break

    table = find_table(table_name, data["compartmentId"])
    rows = table["_rows"]

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
def delete_row(date, table_name):

    table = find_table(table_name, request.args["compartmentId"])

    keys = request.args.getlist("key")
    k = {}
    for key in keys:
        i = key.split(":")
        k[i[0]] = i[1]

    for row in table["_rows"]:
        found = True
        for key in k:
            print(key, row[key], k[key])
            if str(row[key]) != k[key]:
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
