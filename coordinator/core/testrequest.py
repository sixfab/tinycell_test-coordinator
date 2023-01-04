"""Module for processing test request from slack."""

import time
from .yamlio import write_yaml
from .config import (
    config,
    test_process_reloaded,
    test_process_list,
    device_list,
    PROCESS_LIST_PATH,
)
from .testprocess import TestProcess

old_test_process_list = []
logger = config.get("logger")


def reload_test_processes() -> None:
    """Reload test processes from process_list.yaml."""

    for process in test_process_reloaded:
        test_process = TestProcess(
            request_id=process.get("request_id"),
            process_id=process.get("process_id"),
            device_name=process.get("device_name"),
            device_port=process.get("device_port"),
            script_name=process.get("script_name"),
            repeat=process.get("repeat"),
            interval=process.get("interval"),
            status=process.get("status"),
            start_time=process.get("start_time"),
            end_time=process.get("end_time"),
        )
        test_process_list.append(test_process)
    test_process_reloaded.clear()
    logger.info("Test processes are reloaded from file!")


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

    if test_process_list != old_test_process_list:

        dictionary_list = []
        for process in test_process_list:
            dictionary_list.append(vars(process))

        write_yaml(
            PROCESS_LIST_PATH,
            {"process_list": dictionary_list},
        )

        old_test_process_list.clear()
        old_test_process_list.extend(test_process_list)
        logger.info("Test process list is updated!")


def check_request(request: dict):
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
                repeat=1,
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
