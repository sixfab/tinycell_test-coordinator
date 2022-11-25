"""
Module for reading and writing yaml files.
"""
import yaml


def read_yaml(file):
    """Read all items from yaml file."""
    with open(file, encoding="utf-8") as file_object:
        data = yaml.safe_load(file_object)
    return data


def write_yaml(file, items, clear=True):
    """Write all items to yaml file."""
    if clear:
        with open(file, "w", encoding="utf-8") as file_object:
            yaml.dump(items, file_object, default_flow_style=False)
    else:
        with open(file, "a", encoding="utf-8") as file_object:
            yaml.dump(items, file_object, default_flow_style=False)


def load_yaml(text):
    """Load yaml from text."""
    return yaml.safe_load(text)
