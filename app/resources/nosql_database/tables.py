import uuid
import json
from typing import TypedDict, List, Dict


class TableLimits(TypedDict):
    maxReadUnits: int
    maxWriteUnits: int
    maxStorageInGBs: int


class TableColumn(TypedDict):
    column_name: str
    column_type: str
    default_value: any


class RowParam(TypedDict):
    compartmentId: str
    value: Dict[str, any]


class TableParam(TypedDict):
    name: str
    compartmentId: str
    """
    ddlStatement example:
    '\n    CREATE TABLE table_name ( campo1 string, campo2 number, campo3 string DEFAULT "[]" NOT NULL, campo4 number PRIMARY KEY ( SHARD ( campo1 ), campo2 ) )\n    '
    """
    ddlStatement: str
    tableLimits: TableLimits


class Table(TableParam):
    id: str
    _rows: List[Dict[str, any]]
    _columns: List[TableColumn]
    _primary_keys: List[str]


tables: List[Table] = []


def get_columns(ddl_statement: str) -> List[TableColumn]:
    i = ddl_statement.find("(")

    if i == -1:
        raise Exception("invalid ddl")

    ddl = ddl_statement[i + 1 :]
    fields = ddl.split(",")

    found = False

    for i, field in enumerate(fields):
        if "PRIMARY KEY" in field:
            found = True
            break

    if not found:
        raise Exception("no primary keys on ddl")

    fields = fields[0:i]

    _columns: List[TableColumn] = []

    valid_column_types = [
        "integer",
        "string",
        "boolean",
        "double",
        "float",
        "long",
        "number",
        "timestamp",
        "binary",
        "json",
    ]

    for field in fields:
        field = field.strip()
        i = field.find(" ")
        if i == -1:
            raise Exception("no column name")

        column_name = field[0:i]
        field = field[i + 1 :].strip()

        i = field.find(" ")

        if i == -1:
            column_type = field
            field = ""
        else:
            column_type = field[0:i]
            field = field[i + 1 :].strip()

        if column_type not in valid_column_types:
            raise Exception("invalid column type")

        if field and ("DEFAULT" not in field or "NOT NULL" not in field):
            raise Exception("invalid column info")

        default_value = None

        if field:
            field = field.replace("DEFAULT", "")
            field = field.replace("NOT NULL", "")
            field = field.replace('"', "").strip()
            default_value = field
            if column_type in ["number", "long", "float"]:
                default_value = float(default_value)
            if column_type in ["integer"]:
                default_value = int(default_value)
            if column_type in ["boolean"] and default_value == "true":
                default_value = True
            if column_type in ["boolean"] and default_value == "false":
                default_value = False
            if column_type in ["json"]:
                default_value = json.loads(default_value)

        _columns.append(
            {
                "column_name": column_name,
                "column_type": column_type,
                "default_value": default_value,
            }
        )
    return _columns


def get_primary_keys(table: Table) -> List[str]:
    index = table["ddlStatement"].find("PRIMARY KEY")

    if index == -1:
        raise Exception("theres no primary key")

    crop = table["ddlStatement"][index + len("PRIMARY KEY") :]

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

    for column in columns:
        found = False
        for field in table["_columns"]:
            if column == field["column_name"]:
                found = True
                break

        if not found:
            raise Exception("Primary key does not exist on column list")

    return columns


def put_row_on_table(table: Table, data: RowParam):
    primary_keys = table["_primary_keys"]
    found = False

    for primary_key in table["_primary_keys"]:
        if primary_key not in data["value"]:
            raise Exception("row doesnt contain primary key values")

    for i in range(len(table["_rows"])):
        row = table["_rows"][i]
        match = 0
        for primary_key in primary_keys:
            if row[primary_key] == data["value"][primary_key]:
                match += 1

        if match == len(primary_keys):
            found = True
            break

    new_data = {}
    for column in table["_columns"]:
        value = (
            data["value"][column["column_name"]]
            if column["column_name"] in data["value"]
            else None
        )

        if value is None:
            value = column["default_value"]
            new_data[column["column_name"]] = value
            continue

        new_data[column["column_name"]] = value

        print("valor", new_data[column["column_name"]])

        if (
            column["column_type"] in ["boolean"]
            and value not in ["true", "false"]
            and type(value) != bool
        ):
            raise Exception("invalid boolean value")

        if column["column_type"] in ["number", "long", "float"]:
            new_data[column["column_name"]] = float(value)
        if column["column_type"] in ["integer"]:
            new_data[column["column_name"]] = int(value)
        if (
            column["column_type"] in ["boolean"]
            and new_data[column["column_name"]] == "true"
        ):
            new_data[column["column_name"]] = True
        if (
            column["column_type"] in ["boolean"]
            and new_data[column["column_name"]] == "false"
        ):
            new_data[column["column_name"]] = False
        if column["column_type"] in ["json"] and type(value) == str:
            new_data[column["column_name"]] = json.loads(value)

    if not found:
        table["_rows"].append(new_data)
    else:
        table["_rows"][i] = new_data


def add_table(table: TableParam):
    new_table: Table = {
        "id": f"ocid1.nosqltable.oc1.sa-saopaulo-1.{uuid.uuid4()}",
        "_rows": [],
        "compartmentId": table["compartmentId"],
        "ddlStatement": table["ddlStatement"],
        "name": table["name"],
        "tableLimits": table["tableLimits"],
    }
    new_table["_columns"] = get_columns(table["ddlStatement"])
    new_table["_primary_keys"] = get_primary_keys(new_table)
    tables.append(new_table)


def find_table(table_name_or_id: str, compartment_id: str) -> Table:
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

    raise Exception("Table not found.")


def remove_table(table: Table):
    tables.remove(table)


def find_row(rows: List[Dict[str, any]], keys: List[str]):
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
