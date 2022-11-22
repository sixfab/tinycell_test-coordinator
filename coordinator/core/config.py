"""Global Config Module"""

import os
from dotenv import load_dotenv

from .logger import logger
from .yamlio import read_yaml, write_yaml

config = {}
device_list = []
test_process_list = []

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

TEMP_PATH = os.path.expanduser("~") + "/.tinycell_test-coordinator"
FILE_DATABASE_PATH = f"{TEMP_PATH}/database.yaml"
GIT_REPO_PATH = f"{TEMP_PATH}/test-process"
EXECUTABLE_PATH = f"{TEMP_PATH}/test-process/testprocess"


if not os.path.exists(FILE_DATABASE_PATH):
    logger.debug("Creating database file.")
    write_yaml(FILE_DATABASE_PATH, {})

config["database"] = read_yaml(FILE_DATABASE_PATH)
config["slack_bot_token"] = SLACK_BOT_TOKEN
config["slack_app_token"] = SLACK_APP_TOKEN
config["logger"] = logger
