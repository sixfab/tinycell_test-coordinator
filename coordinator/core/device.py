"""Module for holding device attributes"""


class Device:
    """Class for holding Device attributes"""

    def __init__(self, name: str, port: str, availibility: bool) -> None:
        self.name = name
        self.port = port
        self.availibility = availibility

    def __str__(self) -> str:
        return (
            f"\nDevice("
            f"Name: {self.name}, "
            f"Port: {self.port}, "
            f"Availibility: {self.availibility}"
            f")\n"
        )

    def __repr__(self) -> str:
        return (
            f"\nDevice("
            f"Name: {self.name}, "
            f"Port: {self.port}, "
            f"Availibility: {self.availibility}"
            f")\n"
        )
