import json
import os

def saveAsJson(data, filename, jsonIndent=2):
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=jsonIndent)


def load_config(filename):
    print("load_config: " + filename)
    if not os.path.exists(filename):
        print (filename, "not exist!")
        return {}

    config_data = {}
    with open(filename, encoding="UTF-8") as json_file:
        config_data = json.load(json_file)
    return config_data