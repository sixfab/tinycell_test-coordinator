"""Module for holding test process attributes and methods."""

from .config import test_proccess_list


class TestProcess:
    """Class for holding test process attributes and methods."""

    def __init__(
        self,
        proccess_id: str,
        device_name: str,
        script_path: str,
        repeat: int,
        interval: int,
        status: str = "idle",
    ) -> None:

        self.proccess_id = proccess_id
        self.device_name = device_name
        self.script_path = script_path
        self.repeat = repeat
        self.interval = interval
        self.status = status

    def __str__(self) -> str:
        return (
            f"TestProcess("
            f"{self.proccess_id}, "
            f"{self.device_name}, "
            f"{self.script_path}, "
            f"{self.repeat}, {self.interval}, {self.status})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def create(self) -> None:
        """Create a new test process."""
        # TODO: Create a new test process here
        # TODO: Add the new test process to test_proccess_list
        # TODO: Update the status of the test process to "running"
        print(f"{self.proccess_id} is created.")

    def kill(self) -> None:
        """Kill a test process."""
        # TODO: Kill a test process here
        # TODO: Remove the test process from test_proccess_list
        # TODO: Update the status of the test process to "killed"
        print(f"{self.proccess_id} is killed.")
