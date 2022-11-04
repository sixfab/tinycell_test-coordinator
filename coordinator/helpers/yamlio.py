"""
Module for reading and writing yaml files.
"""
import yaml


def read_yaml_all(file):
    with open(file) as file_object:
        data = yaml.safe_load(file_object)
        return data or {}


def write_yaml_all(file, items, clear=True):
    if clear:
        with open(file, "w") as file_object:
            yaml.dump(items, file_object, default_flow_style=False)
    else:
        with open(file, "a") as file_object:
            yaml.dump(items, file_object, default_flow_style=False)
