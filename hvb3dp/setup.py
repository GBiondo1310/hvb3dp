import json
from os import listdir
from ._consts import PRINTERS_JSON


def default_printer():
    """Adds a default custom printer in printers.json file
    in printers.json"""
    with open("printers.json", mode="w") as printers_file:
        json.dump(PRINTERS_JSON, printers_file)
