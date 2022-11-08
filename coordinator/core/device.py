"""Module for holding device attributes"""


class Device:
    """Class for holding Device attributes"""

    def __init__(self, name: str, port: str, availibility: bool) -> None:
        self.name = name
        self.port = port
        self.availibility = availibility
