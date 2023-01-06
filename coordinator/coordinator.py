"""Module for coordinate the creating and removing test processes."""
import threading

from core.config import config
from core.slack import get_slack_socket_mode_handler
from core.git import clone_repo, update_repo
from core.serialport import update_device_list
from core.testrequest import tidy_up_process_list, manage_test_processes, reload_test_processes


logger = config["logger"]
logger.info("Coordinator started")

slack_handler = get_slack_socket_mode_handler()


def source_manager():
    """Thread function for managing git source and device farm."""
    logger.info("Source manager started.")
    # git repo
    clone_repo()
    update_repo()

    # test process
    reload_test_processes()

    while True:
        update_device_list()
        tidy_up_process_list()
        manage_test_processes()
        threading.Event().wait(5)


if __name__ == "__main__":
    threading.Thread(target=source_manager).start()
    slack_handler.start()
