import uuid

tables = []


def add_table(table):
    table["_rows"] = []
    table["id"] = f"ocid1.nosqltable.oc1.sa-saopaulo-1.{uuid.uuid4()}"
    tables.append(table)


def find_table(table_name, compartment_id):
    if table_name.startswith("ocid1.nosqltable.oc1."):
        for table in tables:
            if table_name == table["id"]:
                return table
    else:
        for table in tables:
            if table["name"] == table_name and table["compartmentId"] == compartment_id:
                return table

    return None


def remove_table(table):
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
