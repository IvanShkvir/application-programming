import json


def get_value_from_json(json_data, field_name):
    items = json.dumps(json_data)
    array = json.loads(items)
    return array[field_name]
