"""Module for holding test process attributes and methods."""
import os
import signal
import threading
import subprocess
from dataclasses import dataclass
from .config import config, EXECUTABLE_PATH

logger = config["logger"]


class TestProcess:
    """Class for holding test process attributes and methods."""

    @dataclass
    class Status:
        """Class for holding test process status"""

        IDLE: str = "idle"
        RUNNING: str = "running"
        FINISHED: str = "finished"
        TERMINATED: str = "terminated"
        KILLED: str = "killed"

    process_id = 0

    def __init__(
        self,
        request_id: str,
        device_name: str,
        device_port: str,
        script_name: str,
        repeat: int,
        interval: int,
        status: str = Status.IDLE,
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

        def on_exit(process) -> None:
            """After a test process ends, update the status of the test process."""
            logger.info(
                f"{self.process_id} on {self.device_port} is waiting for exit."
            )
            process.wait()
            if self.status == self.Status.RUNNING:
                self.status = self.Status.FINISHED
                logger.info(f"{self.process_id} is finished.")
            else:
                logger.info(
                    f"{self.process_id} is {self.status} by another request."
                )

        command = f"python3 run.py -t {self.script_name} -p {self.device_port}"
        process = subprocess.Popen(
            command,
            cwd=EXECUTABLE_PATH,
            start_new_session=True,  # to seperate from parent process group
            close_fds=True,
            shell=True,
        )
        self.process_id = process.pid
        self.status = self.Status.RUNNING
        logger.info(f"{self.process_id} is created.")

        threading.Thread(target=on_exit, args=(process,)).start()
        process.communicate()

    def terminate(self) -> None:
        """Terminate a test process gracefully."""

        def terminate_process() -> None:
            """Terminate a process by its process id."""
            try:
                os.kill(self.process_id, signal.SIGTERM)
            except ProcessLookupError:
                ...
            else:
                self.status = self.Status.TERMINATED
                logger.info(f"{self.process_id} is terminated.")

        logger.info(f"{self.process_id} is terminating...")
        threading.Thread(target=terminate_process).start()

    def kill(self) -> None:
        """Kill a test process."""

        def kill_process() -> None:
            """Kill a process by its process id."""
            try:
                os.kill(self.process_id, signal.SIGKILL)
            except ProcessLookupError:
                ...
            else:
                self.status = self.Status.KILLED
                logger.info(f"{self.process_id} is killed.")

        logger.info(f"{self.process_id} is killing...")
        threading.Thread(target=kill_process).start()
