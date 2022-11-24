"""Module for processing test request from slack."""

import time
from .config import test_process_list, device_list
from .testprocess import TestProcess


def tidy_up_process_list() -> None:
    """Remove the test processes that are already finished from the list."""
    must_remove_list = []
    for process in test_process_list:
        if (
            process.status == TestProcess.Status.FINISHED
            or process.status == TestProcess.Status.TERMINATED
            or process.status == TestProcess.Status.KILLED
        ):
            must_remove_list.append(process)

    for process in must_remove_list:
        test_process_list.remove(process)


def check_request(request: dict) -> None:
    """Create and remove test_processes by getting request from slack."""

    is_valid_request = False
    is_existed_device = False

    tidy_up_process_list()

    request_id = f"request_{int(time.time())}"
    request_type = request.get("request_type")
    device_name = request.get("device_name")
    device_port = request.get("device_port")
    script_name = request.get("script_name")
    repeat = request.get("repeat")
    interval = request.get("interval")

    # if device port is not specified, decide the port by device name
    if device_port is None:
        for device in device_list:
            if device.name == device_name:
                device_port = device.port
                break

    # is it a valid request?
    if (
        (device_port or device_name)
        and script_name
        and request_type is not None
    ):
        is_valid_request = True
    else:
        raise Exception("Invalid request. Missing some required fields!")

    # is it a existed device?
    for device in device_list:
        if device.port == device_port:
            is_existed_device = True
            break

    if not is_existed_device:
        raise Exception("Invalid request. Device not found!")

    if is_valid_request and is_existed_device:
        if request_type == "create":
            # raise exception if the test device is already occupied
            for process in test_process_list:
                if (
                    process.device_name == device_name
                    or process.device_port == device_port
                ):
                    raise Exception("Target device is already in use!")

            test_process = TestProcess(
                request_id=request_id,
                device_name=device_name,
                device_port=device_port,
                script_name=script_name,
                repeat=repeat,
                interval=interval,
            )
            test_process_list.append(test_process)
            test_process.create()
            return f"Test process running on {device_name} is completed!"

        # request_type is "delete"
        elif request_type == "delete":
            is_existed = False

            for process in test_process_list:
                if (
                    process.device_name == device_name
                    or process.device_port == device_port
                ):
                    is_existed = True
                    process.terminate()
                    break

            if not is_existed:
                raise Exception("Target device is not in use!")
            else:
                return (
                    f"Test process running on {device_name} "
                    f"is terminated gracefully!"
                )

        # request_type is "force_delete"
        elif request_type == "force_delete":
            is_existed = False
            for process in test_process_list:
                if (
                    process.device_name == device_name
                    or process.device_port == device_port
                ):
                    is_existed = True
                    process.kill()
                    break

            if not is_existed:
                raise Exception("Target device is not in use!")
            else:
                return (
                    f"Test process running on {device_name} killed immediately!"
                )
