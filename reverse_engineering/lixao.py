from typing import List
from enum import Enum


class Operator(Enum):
    GTE = "GTE"
    LTE = "LTE"
    GT = "GT"
    LT = "LT"
    EQ = "EQ"


class QueryFilter(object):
    def __init__(self, column, value, operator) -> None:
        self.column: str = column
        self.value: any = value
        self.operator: Operator = operator

    def __repr__(self) -> str:
        return f"QueryFilter(column={self.column}, value={self.value}, operator={self.operator})"


DETECTIONS_TABLE_NAME = "table_name"
req_id = "abjiahiha"
timestamp = 171718718

query = f"SELECT * FROM {DETECTIONS_TABLE_NAME} WHERE requisition_id = '{req_id}' and timestamp >= {timestamp} and hidden = false ORDER BY timestamp ASC"

index = query.find("FROM")

if index == -1:
    raise Exception("theres no FROM on query")

query = query[index + len("FROM") :].strip()
index = query.find(" ")

table_name = ""

if index == -1:
    table_name = query
    query = ""
else:
    table_name = query[:index]
    query = query[index + 1 :]

if table_name == "":
    raise Exception("there no table name on query")

index_where = query.find("WHERE")
index_order_by = query.find("ORDER BY")

filters: List[QueryFilter] = []

if index_order_by != -1:
    query_order = query[index_order_by + len("ORDER BY") :].strip()
    query = query[:index_order_by].strip()

if index_where != -1:
    query_filter = query[index + len("WHERE") :].strip()

    where_arguments = query_filter.split("and")

    for where_argument in where_arguments:
        if ">=" in where_argument:
            column, value = where_argument.split(">=")
            filters.append(
                QueryFilter(
                    column=column.strip(), value=value.strip(), operator=Operator.GTE
                )
            )
            continue
        if "<=" in where_argument:
            column, value = where_argument.split("<=")
            filters.append(
                QueryFilter(
                    column=column.strip(), value=value.strip(), operator=Operator.LTE
                )
            )
            continue
        if "=" in where_argument:
            column, value = where_argument.split("=")
            filters.append(
                QueryFilter(
                    column=column.strip(), value=value.strip(), operator=Operator.EQ
                )
            )
            continue
        if ">" in where_argument:
            column, value = where_argument.split(">")
            filters.append(
                QueryFilter(
                    column=column.strip(), value=value.strip(), operator=Operator.GT
                )
            )
            continue
        if "<" in where_argument:
            column, value = where_argument.split("<")
            filters.append(
                QueryFilter(
                    column=column.strip(), value=value.strip(), operator=Operator.LT
                )
            )
            continue

print(table_name)
print(filters)
print(query_order)