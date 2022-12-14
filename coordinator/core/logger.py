"""Module for logger configuration."""
import os
import logging
import logging.handlers

LOG_PATH = os.path.expanduser("~") + "/.tinycell_test-coordinator/logs"
LOG_FORMAT = "%(asctime)s --> %(filename)-18s %(levelname)-8s %(message)s"

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

logger = logging.getLogger("tinycell_test-coordinator")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOG_FORMAT)

# Handler for logging to file.
log_handler = logging.handlers.TimedRotatingFileHandler(
    filename=f"{LOG_PATH}/coordinator-log", when="midnight", backupCount=6
)
log_handler.setFormatter(formatter)
log_handler.set_name("log_handler")
logger.addHandler(log_handler)

# Handler for logging to console.
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.set_name("console_handler")
logger.addHandler(console_handler)
