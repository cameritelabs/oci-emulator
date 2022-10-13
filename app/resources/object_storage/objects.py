from typing import Tuple


def get_objects(
    bucket: dict,
    prefix: str = None,
    start: str = None,
    end: str = None,
    delimiter: str = None,
) -> Tuple[list, list]:
    _objects = [
        {"name": _object["object_name"], "etag": _object["etag"]}
        for _object in bucket["_objects"]
    ]
    _prefixes = []

    if prefix is not None:
        _objects = [_obj for _obj in _objects if _obj["name"].startswith(prefix)]

    if start is not None:
        _objects = [_obj for _obj in _objects if _obj["name"] >= start]

    if end is not None:
        _objects = [_obj for _obj in _objects if _obj["name"] <= end]

    if delimiter is not None:
        for _obj in _objects:
            if (
                delimiter in _obj["name"]
                and _obj["name"].split(delimiter)[0] + "/" not in _prefixes
            ):
                _prefixes.append(_obj["name"].split(delimiter)[0] + "/")

        _objects = [_obj for _obj in _objects if delimiter not in _obj["name"]]

    return _objects, _prefixes
