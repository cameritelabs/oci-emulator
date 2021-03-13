tables = []


def add_table(table):
    table["_rows"] = []
    tables.append(table)


def find_table(table_name, compartment_id):
    for table in tables:
        if table["name"] == table_name and table["compartmentId"] == compartment_id:
            return table

    return None


def remove_table(table):
    tables.remove(table)
