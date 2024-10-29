import json


def read_json(json_path: str):
    f = open(json_path, "r")
    data_config = json.load(f)
    f.close()

    return data_config


def save_json(dict_: dict, json_path: str):
    with open(json_path, "w") as outfile:
        json.dump(dict_, outfile, indent=4)
