"""Module for slack api"""
import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .config import config
from .yamlio import load_yaml
from .testrequest import check_request
from .git import update_repo, switch_desired_branch, fetch_repo
from .config import device_list, test_process_list

logger = config["logger"]

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
SLACK_COMMAND_CHANNEL = os.environ.get("SLACK_COMMAND_CHANNEL")
SLACK_REPORT_CHANNEL = os.environ.get("SLACK_REPORT_CHANNEL")


# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)
web_client = app.client


@app.message("hello")
def message_hello(message, say):
    """Message hello handler"""
    say(text=f"Hey there <@{message['user']}>!")


@app.message("device")
def message_devices(message, say):
    """Message devices handler"""

    response = "Devices:\n"

    for device in device_list:
        response += f"Name: {device.name}\t" f"Port: {device.port}\n\n"

    say(text=response)


@app.message("test process")
def message_test_process(message, say):
    """Message test process handler"""
    response = "Test Processes:\n"

    for process in test_process_list:
        response += (
            f"*********************************\n"
            f"Request ID: {process.request_id}\n"
            f"Process ID: {process.process_id}\n"
            f"Device Name: {process.device_name}\n"
            f"Device Port: {process.device_port}\n"
            f"Script Name: {process.script_name}\n"
            f"Status: {process.status}\n"
            f"Start Time: {process.start_time}\n"
            f"End Time: {process.end_time}\n"
            f"Repeat: {process.repeat}\n"
            f"Interval: {process.interval}\n"
            f"Start On: {process.start_on}\n"
            f"Run Until: {process.run_until}\n"
            f"*********************************\n\n"
        )
    say(text=response)


@app.message("fetch repo")
def message_fetch_repo(message, say):
    """Message fetch repo handler"""
    try:
        fetch_repo()
    except Exception as error:
        logger(f"Error: {error}")
        say(text=f"Error: {error}")
    else:
        logger.info("Fetched all changes from test_process repo succesfully")
        say(text="Info: Fetched all changes from test_process repo succesfully")


@app.message("update branch to")
def message_update_branch(message, say):
    """Message update branch handler"""
    branch_name = message["text"].split(" ")[-1]
    try:
        switch_desired_branch(branch=branch_name)
    except Exception as error:
        logger(f"Error: {error}")
        say(text=f"Error: {error}")
    else:
        logger.info("test_process branch updated succesfully to " + branch_name)
        say(text="Info: test_process branch updated succesfully to " + branch_name)


@app.message("update repo")
def message_update_repo(message, say):
    """Message update repo handler"""

    try:
        update_repo()
    except Exception as error:
        logger(f"Error: {error}")
        say(text=f"Error: {error}")
    else:
        logger.info("test_process repo updated succesfully")
        say(text="Info: test_process repo updated succesfully")


@app.event({"type": "message", "subtype": "file_share"})
def handle_message_events(body):
    """Handle file shared event"""
    url = body["event"]["files"][0]["url_private"]

    response = requests.get(url, headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}, timeout=30)

    if response.status_code == 200:
        logger.info("Yaml file downloaded successfully")
        yaml = load_yaml(response.text)

        try:
            request_list = yaml["requests"]
        except Exception as error:
            logger.error(f"Error: {error}")
            web_client.chat_postMessage(channel=SLACK_COMMAND_CHANNEL, text=f"Error: {error}")
        else:
            for request in request_list:
                print(request)
                try:
                    result = check_request(request)
                except Exception as error:
                    logger.error(f"Error: {error}")
                    web_client.chat_postMessage(
                        channel=SLACK_COMMAND_CHANNEL, text=f"Error: {error}"
                    )
                else:
                    logger.info("Test request processed successfully")
                    web_client.chat_postMessage(
                        channel=SLACK_COMMAND_CHANNEL, text=f"Info: {result}"
                    )
    else:
        raise Exception("Failed to download yaml file from slack!")


def get_slack_socket_mode_handler():
    """Get slack socket mode handler"""
    return SocketModeHandler(app, SLACK_APP_TOKEN)
