"""Module for processing test request from slack."""

import time
from .config import test_process_list
from .testprocess import TestProcess


def tidy_up_process_list() -> None:
    """Remove the test processes that are already finished from the list."""
    must_remove_list = []
    for process in test_process_list:
        if process.status == "finished":
            must_remove_list.append(process)

    for process in must_remove_list:
        test_process_list.remove(process)


def check_request(request: dict) -> TestProcess:
    """Create and remove test_processes by getting request from slack."""

    tidy_up_process_list()

    request_id = f"request_{int(time.time())}"
    request_type = request.get("request_type")
    device_name = request.get("device_name")
    device_port = request.get("device_port")
    script_name = request.get("script_name")
    repeat = request.get("repeat")
    interval = request.get("interval")

    # is it a valid request?
    if request_type and device_port and script_name:
        test_process_remove_list = []
        if request_type == "delete":
            for process in test_process_list:
                if process.device_name == device_name:
                    process.kill(process.process_id)
                    test_process_remove_list.append(process)

            # remove the test process from the list after iteartion ends
            for process in test_process_remove_list:
                test_process_list.remove(process)

        if request_type == "create":
            # raise exception if the test device is already occupied
            for process in test_process_list:
                if process.device_name == device_name:
                    raise Exception("Target device is already in use!")

            test_process = TestProcess(
                request_id=request_id,
                device_name=device_name,
                device_port=device_port,
                script_name=script_name,
                repeat=repeat,
                interval=interval,
            )
            test_process.create()
            test_process_list.append(test_process)
