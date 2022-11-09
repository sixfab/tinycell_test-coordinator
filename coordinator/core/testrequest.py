"""Module for processing test request from slack."""

import time
from .config import test_proccess_list
from .testprocess import TestProcess


def check_request(request: dict) -> TestProcess:
    """Create and remove test_processes by getting request from slack."""

    request_id = f"request_{int(time.time())}"
    request_type = request.get("request_type")
    test_device = request.get("test_device")
    test_script = request.get("test_script")
    repeat = request.get("repeat")
    interval = request.get("interval")

    # is it a valid request?
    if request_type and test_device and test_script:
        test_process_remove_list = []
        if request_type == "delete":
            for proccess in test_proccess_list:
                if proccess.device_name == test_device:
                    proccess.kill(proccess.proccess_id)
                    test_process_remove_list.append(proccess)

            # remove the test process from the list after iteartion ends
            for proccess in test_process_remove_list:
                test_proccess_list.remove(proccess)

        if request_type == "create":
            # raise exception if the test device is already occupied
            for process in test_proccess_list:
                if process.device_name == test_device:
                    raise Exception("Target device is already in use!")

            test_process = TestProcess(
                proccess_id=request_id,
                device_name=test_device,
                script_path=test_script,
                repeat=repeat,
                interval=interval,
            )
            test_process.create()
            test_proccess_list.append(test_process)
