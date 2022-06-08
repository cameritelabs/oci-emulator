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


def add_table(table: TableParam):
    print(table)

    table["_rows"] = []
    table["id"] = f"ocid1.nosqltable.oc1.sa-saopaulo-1.{uuid.uuid4()}"
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
