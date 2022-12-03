# Device Farm Service for Testing Tinycells
The program is a Slack bot service which can be used to test multiple Tinycell devices in predesigned scenarios. It is suggested to connect the bot into two different channels which are used to control the devices and to monitor the test results status.

### Bot Commands
* `hello` - bot will reply with `Hey there @username!`.
* `device` - bot will reply with connected device list.
* `update repo` - bot will update the TestProcess repo from GitHub to retrive new test cases.

### Slack Configuration
* Create a Slack bot with given manifest file and get your `APP_TOKEN` and `BOT_TOKEN`.
* Add this app/bot to your Slack channels which you would like to interract with bot.

    ```yaml
    display_information:
    name: [SLACK_APP_NAME]
    description: [SLACK_APP_DESCRIPTION]
    background_color: "[SLACK_APP_BACKGROUND_COLOR_HEX]"
    features:
    bot_user:
        display_name: [SLACK_BOT_NAME]
        always_online: false
    oauth_config:
    scopes:
        bot:
        - chat:write
        - files:read
        - groups:history
    settings:
    event_subscriptions:
        bot_events:
        - file_change
        - file_created
        - message.groups
    interactivity:
        is_enabled: true
    org_deploy_enabled: false
    socket_mode_enabled: true
    token_rotation_enabled: false
    ```

---
<br>

## Example Environment File
A `.env` file is neccessary to run the program. It should be placed in the same directory with repo (`/opt/sixfab/tinycell/tinycell_test-coordinator`). The file should contain the following information.
```bash
# .env
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-x-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx

TEST_PROCESS_REPO=https://github.com/sixfab/tinycell_test-process.git
TEST_PROCESS_BRANCH=dev

SLACK_COMMAND_CHANNEL="#tinycell-command"
SLACK_REPORT_CHANNEL="#tinycell-reports"
```

## Manual Installation
By following these steps, you can configure the program to run on each boot.
```bash
# Create a sixfab user, give it the neccessary permissons.
~$ sudo adduser --disabled-password --gecos "" sixfab &> /dev/null
~$ echo "sixfab ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/sixfab_tinycell &> /dev/null
~$ sudo usermod -a -G dialout sixfab

# Clone repo to any directory.
~$ git clone https://github.com/sixfab/tinycell_test-coordinator.git

# Copy the program files into /opt/sixfab/tinycell directory.
~$ sudo mkdir -p /opt/sixfab/tinycell
~$ sudo mv tinycell_test-coordinator /opt/sixfab/tinycell/

# Go to the program directory.
~$ cd /opt/sixfab/tinycell/tinycell_test-coordinator

# Create a virtual environment, activate it.
~$ python3 -m venv venv    # OR "virtualenv ."
~$ source venv/bin/activate

# Install the required packages.
(venv) ~$ pip install -r requirements.txt

# Create a .env file and fill it with your Slack tokens.
(venv) ~$ sudo vim .env

# Install the systemd service file.
(venv) ~$ sudo cp tinycell_test-coordinator.service /etc/systemd/system/
# Give the service file the sixfab user permissions.
(venv) ~$ sudo chown sixfab /etc/systemd/system/tinycell_test-coordinator.service

# Reload the systemd daemon.
(venv) ~$ sudo systemctl daemon-reload
# Enable and start the service.
(venv) ~$ sudo systemctl enable tinycell_test-coordinator.service
(venv) ~$ sudo systemctl start tinycell_test-coordinator.service
```

## Debugging
You can check the status of the service with the following command.
```bash
~$ sudo systemctl status tinycell_test-coordinator.service
```

You can debug the program with the following command.
```bash
~$ sudo journalctl -u tinycell_test-coordinator.service -f
```





