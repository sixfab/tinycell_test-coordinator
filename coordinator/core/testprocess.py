"""Module for holding test process attributes and methods."""
import threading
import subprocess
from .config import config, EXECUTABLE_PATH

logger = config["logger"]


class TestProcess:
    """Class for holding test process attributes and methods."""

    process_id = 0

    def __init__(
        self,
        request_id: str,
        device_name: str,
        device_port: str,
        script_name: str,
        repeat: int,
        interval: int,
        status: str = "idle",
    ) -> None:
        self.request_id = request_id
        self.device_name = device_name
        self.device_port = device_port
        self.script_name = script_name
        self.repeat = repeat
        self.interval = interval
        self.status = status

    def __str__(self) -> str:
        return (
            f"TestProcess("
            f"{self.request_id}, "
            f"{self.process_id}, "
            f"{self.device_name}, "
            f"{self.script_name}, "
            f"{self.repeat}, {self.interval}, {self.status})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def create(self) -> None:
        """Create a new test process."""

        command = f"python3 run.py -t {self.script_name} -p {self.device_port}"
        process = subprocess.Popen(
            command,
            cwd=EXECUTABLE_PATH,
            start_new_session=True,  # to seperate from parent process group
            close_fds=True,
            shell=True,
        )
        self.process_id = process.pid
        self.status = "running"
        logger.info(f"{self.process_id} is created.")

        threading.Thread(target=self.on_exit, args=(process,)).start()
        process.communicate()

    def on_exit(self, process) -> None:
        """After a test process ends, update the status of the test process."""
        logger.info(
            f"{self.process_id} on {self.device_port} is waiting for exit."
        )
        process.wait()
        self.status = "finished"
        logger.info(f"{self.process_id} is finished.")

    def kill(self) -> None:
        """Kill a test process."""
        # TODO: Kill a test process here
        # TODO: Remove the test process from test_proccess_list
        # TODO: Update the status of the test process to "killed"
        print(f"{self.process_id} is killed.")
