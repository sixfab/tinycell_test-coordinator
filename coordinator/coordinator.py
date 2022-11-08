"""Module for coordinate the creating and removing test processes."""
import threading

from core.config import config
from core.slack import get_slack_socket_mode_handler
from core.git import clone_repo

logger = config["logger"]
logger.info("Coordinator started")

slack_handler = get_slack_socket_mode_handler()


def source_manager():
    """Thread function for managing git source and device farm."""
    logger.info("Source manager started.")
    clone_repo()

    while True:
        pass


if __name__ == "__main__":
    threading.Thread(target=source_manager).start()
    slack_handler.start()
