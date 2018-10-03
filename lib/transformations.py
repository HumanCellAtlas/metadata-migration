def move(obj, source_field_path, destination_field_path):
    parent = get_parent(obj, source_field_path)
    source_field_path_parts = _path_to_parts(source_field_path)
    value = parent[source_field_path_parts[-1]]
    del parent[source_field_path_parts[-1]]
    set(obj, destination_field_path, value)
    return obj


def pounds_to_kilograms(obj, value_path, unit_path):
    unit = get(obj, unit_path)
    value = float(get(obj, value_path))
    if unit == 'lbs':
        set(obj, value_path, str(value * 0.453592))
        set(obj, unit_path, 'kgs')
    else:
        raise Exception("Unknown unit for conversion!")
    return obj


def set(obj, field_path, value):
    destination_field_path_parts = _path_to_parts(field_path)
    containing_val = obj
    for path_part in destination_field_path_parts[:-1]:
        if path_part not in containing_val:
            containing_val[path_part] = dict()
        containing_val = containing_val[path_part]
    containing_val[destination_field_path_parts[-1]] = value
    return obj


def _path_to_parts(path):
    return path.split('.')


def get_parent(obj, field_path):
    path_parts = _path_to_parts(field_path)
    parent = obj
    for path_part in path_parts[:-1]:
        parent = parent[path_part]
    return parent


def get(obj, field_path):
    result = obj
    for path_part in _path_to_parts(field_path):
        result = result[path_part]
    return result
