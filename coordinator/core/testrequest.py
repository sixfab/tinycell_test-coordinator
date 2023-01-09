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
            start_on=process.get("start_on"),
            run_until=process.get("run_until"),
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
            process.status == TestProcess.Status.COMPLETED
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
    repeat = request.get("repeat", 0)
    interval = request.get("interval", 0)
    start_on = request.get("start_on", int(time.time()))
    run_until = request.get("run_until", 0)

    # if device port is not specified, decide the port by device name
    if device_port is None:
        for device in device_list:
            if device.name == device_name:
                device_port = device.port
                break

    # is it a valid request?
    if (device_port or device_name) and script_name and request_type is not None:
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
                if process.device_name == device_name or process.device_port == device_port:
                    raise Exception("Target device is already in use!")

            test_process = TestProcess(
                request_id=request_id,
                device_name=device_name,
                device_port=device_port,
                script_name=script_name,
                repeat=repeat,
                interval=interval,
                start_on=start_on,
                run_until=run_until,
            )
            test_process.status = TestProcess.Status.WAITING
            test_process_list.append(test_process)
            return f"Test process is added the process list. Request ID: {request_id}"

        # request_type is "delete"
        elif request_type == "delete":
            is_existed = False

            for process in test_process_list:
                if process.device_name == device_name or process.device_port == device_port:
                    is_existed = True
                    process.terminate()
                    break

            if not is_existed:
                raise Exception("Target device is not in use!")
            else:
                return f"Test process running on {device_name} " f"is terminated gracefully!"

        # request_type is "force_delete"
        elif request_type == "force_delete":
            is_existed = False
            for process in test_process_list:
                if process.device_name == device_name or process.device_port == device_port:
                    is_existed = True
                    process.kill()
                    break

            if not is_existed:
                raise Exception("Target device is not in use!")
            else:
                return f"Test process running on {device_name} killed immediately!"


def manage_test_processes():
    """Manage test processes."""

    for process in test_process_list:
        if process.status == TestProcess.Status.WAITING:
            if process.start_on <= time.time():
                process.create()

        if process.status == TestProcess.Status.FINISHED:
            # calculate the next start time
            process.start_on = process.start_on + process.interval

            # Recreate the process if run_until is not 0 and not reached
            if process.run_until != 0 and process.run_until >= time.time():
                run_until_case = True
            else:
                run_until_case = False

            # Recreate the process if repeat is greater than 0 or run_until_case is True
            if process.repeat > 0 or run_until_case:
                process.repeat -= 1
                process.status = TestProcess.Status.REPEATING
            else:
                process.status = TestProcess.Status.COMPLETED

        if process.status == TestProcess.Status.REPEATING:
            # Recreate the process if reached start_on time
            if process.start_on <= time.time():
                process.status = TestProcess.Status.FINISHED
                process.create()
