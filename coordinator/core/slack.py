"""Module for slack api"""
import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .config import config
from .yamlio import load_yaml

logger = config["logger"]

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)
web_client = app.client

# send hello message to tinycell-test channel
# web_client.chat_postMessage(channel="#tinycell-test", text="Hello world!")


@app.message("hello")
def message_hello(message, say):
    """Message hello handler"""
    say(
        text=f"Hey there <@{message['user']}>!",
    )


@app.event({"type": "message", "subtype": "file_share"})
def handle_message_events(body):
    """Handle file shared event"""
    url = body["event"]["files"][0]["url_private"]

    print("URL:", url)

    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        logger.info("Yaml file downloaded successfully")
        yaml = load_yaml(response.text)
        print(yaml)
    else:
        raise Exception("Failed to download yaml file from slack!")


def get_slack_client():
    """Get slack client"""
    return app.client


def get_slack_socket_mode_handler():
    """Get slack socket mode handler"""
    return SocketModeHandler(app, SLACK_APP_TOKEN)
