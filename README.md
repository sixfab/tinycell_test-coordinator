# tinycell_test-device-farm
It is repo for testing multiple tinycell devices in predesigned scenarios.


# Prepration

## Slack api
* Create a slack bot and get `app_token` and `bot_token`.
* Add this bot to your slack channels which you would like to interract with bot.

## Github
* Authorize the host raspberry pi to access your github account.

# Installation
Downlaod install.sh and run it.
`sudo bash ./install.sh`

## Extra Steps for private repos
Clone repo to path
```
git clone git@github.com:sixfab/tinycell_test-coordinator.git
sudo mv tinycell_test-coordinator /opt/sixfab/tinycell/
```

Go to path

`cd /opt/sixfab/tinycell/tinycell_test-coordinator`


Create virtual environment and activate it

`python3 -m venv venv`

`source venv/bin/activate`


Install requirements

`pip3 install -r requirements.txt`


Create .env file. .env must contain following variables

```
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-x-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx

TEST_PROCESS_REPO=git@github.com:sixfab/tinycell_test-process.git
TEST_PROCESS_BRANCH=dev

SLACK_COMMAND_CHANNEL="#tinycell-command"
SLACK_REPORT_CHANNEL="#tinycell-reports"
```

Create deploy key for test-process repo

```
ssh-keygen -t ed25519 -C "your_email@example.com"

eval "$(ssh-agent -s)"

ssh-add ~/.ssh/id_ed25519
```

Copy public key to deploy key section of the repository. For instructions see [here](https://docs.github.com/en/developers/overview/managing-deploy-keys)
```
cat ~/.ssh/id_ed25519.pub
```
**Note: ** You may want to change the name of the key to something more meaningful.

Install service and start it
```
sudo cp tinycell_test-coordinator.service /etc/systemd/system/tinycell_test-coordinator.service

sudo chown sixfab /etc/systemd/system/tinycell_test-coordinator.service

sudo systemctl daemon-reload

sudo systemctl enable tinycell_test-coordinator.service

sudo systemctl start tinycell_test-coordinator.service
```







