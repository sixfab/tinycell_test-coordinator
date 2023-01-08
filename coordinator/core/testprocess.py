"""Module for holding test process attributes and methods."""
import os
import time
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
        WAITING: str = "waiting"
        RUNNING: str = "running"
        FINISHED: str = "finished"
        REPEATING: str = "repeating"
        COMPLETED: str = "completed"
        TERMINATED: str = "terminated"
        KILLED: str = "killed"

    def __init__(
        self,
        request_id: str,
        device_name: str,
        device_port: str,
        script_name: str,
        repeat: int = 0,
        interval: int = 0,
        start_on: int = 0,
        run_until: int = 0,
        status: str = Status.IDLE,
        process_id: int = None,
        start_time: float = 0,
        end_time: float = 0,
    ) -> None:
        self.request_id = request_id
        self.device_name = device_name
        self.device_port = device_port
        self.script_name = script_name
        self.repeat = repeat
        self.interval = interval
        self.start_on = start_on
        self.run_until = run_until
        self.status = status
        self.process_id = process_id
        self.start_time = start_time
        self.end_time = end_time

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
            logger.info(f"{self.process_id} on {self.device_port} is waiting for exit.")
            process.wait()
            if self.status == self.Status.RUNNING:
                self.status = self.Status.FINISHED
                self.end_time = time.time()
                logger.info(f"{self.process_id} is finished.")
            else:
                logger.info(f"{self.process_id} is {self.status} by another request.")

        command = (
            f"../venv/bin/python {EXECUTABLE_PATH}/run.py -t {self.script_name}"
            f" -p {self.device_port}"
        )
        process = subprocess.Popen(
            command,
            start_new_session=True,  # to seperate from parent process group
            close_fds=True,
            shell=True,
        )
        self.process_id = process.pid
        self.status = self.Status.RUNNING
        self.start_time = time.time()
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
                self.end_time = time.time()
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
                self.end_time = time.time()
                logger.info(f"{self.process_id} is killed.")

        logger.info(f"{self.process_id} is killing...")
        threading.Thread(target=kill_process).start()
