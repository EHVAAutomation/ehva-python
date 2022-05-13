""" Ehva Module """
import base64
import json
import sys


def parse_inputs():
    base64_json = sys.argv[1]
    json_string = base64.b64decode(base64_json).decode("UTF-8")
    return json.loads(json_string)


def send_outputs(outputs: dict):
    json_string = json.dumps(outputs)
    json_base64 = base64.b64encode(json_string.encode("utf-8"))
    sys.stdout.write(str(json_base64, "utf-8"))
