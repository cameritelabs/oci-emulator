import uuid

from typing import TypedDict, List, Optional


class TableLimits(TypedDict):
    maxReadUnits: int
    maxWriteUnits: int
    maxStorageInGBs: int


class TableParam(TypedDict):
    name: str
    compartmentId: str
    ddlStatement: str
    tableLimits: TableLimits


class Table(TableParam):
    id: str
    _rows: List[dict]


tables: List[Table] = []


def get_primary_keys(ddl_statement):
    index = ddl_statement.find("PRIMARY KEY")

    if index == -1:
        raise Exception("theres no primary key")

    crop = ddl_statement[index + len("PRIMARY KEY") :]

    start_at = None
    ended_at = None
    open_parenteses_found = 0
    close_parenteses_found = 0

    for i in range(len(crop)):
        letter = crop[i]
        if letter == "(":
            if start_at is None:
                start_at = i
            open_parenteses_found += 1

        if letter == ")":
            close_parenteses_found += 1
            if close_parenteses_found == open_parenteses_found:
                ended_at = i
                break

    if open_parenteses_found != close_parenteses_found:
        raise Exception("invalid primary key")

    crop = crop[start_at + 1 : ended_at]
    columns = crop.split(",")

    for i in range(len(columns)):
        column = columns[i]
        start_parenteses = column.find("(")
        if start_parenteses == -1:
            columns[i] = column.strip()
            continue
        end_parenteses = column.find(")")
        columns[i] = column[start_parenteses + 1 : end_parenteses].strip()

    return columns


def add_table(table: TableParam):
    print(table)

    table["_rows"] = []
    table["id"] = f"ocid1.nosqltable.oc1.sa-saopaulo-1.{uuid.uuid4()}"
    table["_primary_keys"] = get_primary_keys(table["ddlStatement"])
    tables.append(table)


def find_table(table_name_or_id: str, compartment_id: str) -> Optional[Table]:
    if table_name_or_id.startswith("ocid1.nosqltable.oc1."):
        for table in tables:
            if table_name_or_id == table["id"]:
                return table
    else:
        for table in tables:
            if (
                table["name"] == table_name_or_id
                and table["compartmentId"] == compartment_id
            ):
                return table

    return None


def remove_table(table: Table):
    tables.remove(table)


def find_row(rows, keys):
    for row in rows:
        equal = True
        for key in keys:
            if key not in row:
                return None

            if type(keys[key]) != type(row[key]):
                keys[key] = type(row[key])(keys[key])
            if row[key] != keys[key]:
                equal = False
                break

        if equal:
            return row
    return None
