"""Global Config Module"""

import os
from dotenv import load_dotenv

from .logger import logger
from .yamlio import read_yaml, write_yaml

config = {}

load_dotenv()

# SLACK CONFIGS
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
SLACK_COMMAND_CHANNEL = os.environ.get("SLACK_COMMAND_CHANNEL")
SLACK_REPORT_CHANNEL = os.environ.get("SLACK_REPORT_CHANNEL")

TEMP_PATH = os.path.expanduser("~") + "/.tinycell_test-coordinator"

# GIT CONFIGS
GIT_REMOTE_LINK = (
    os.environ.get("TEST_PROCESS_REPO") \
        or "git@github.com:sixfab/tinycell_test-process.git"
)
GIT_REPO_BRANCH = "dev"
GIT_REPO_PATH = f"{TEMP_PATH}/test-process"

EXECUTABLE_PATH = f"{TEMP_PATH}/test-process/testprocess"
PROCESS_LIST_PATH = f"{TEMP_PATH}/process_list.yaml"

if not os.path.exists(PROCESS_LIST_PATH):
    logger.debug("Creating process_list file.")
    write_yaml(PROCESS_LIST_PATH, {"process_list": []})

test_process_list = []
device_list = []

test_process_reloaded = read_yaml(PROCESS_LIST_PATH).get("process_list", [])


config["slack_bot_token"] = SLACK_BOT_TOKEN
config["slack_app_token"] = SLACK_APP_TOKEN
config["logger"] = logger
