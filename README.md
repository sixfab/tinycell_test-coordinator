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

## Extra Steps for private repos
Clone repo to path
`git clone https://github.com/sixfab/tinycell_test-coordinator /opt/sixfab/tinycell/`

Go to path
`cd /opt/sixfab/tinycell/tinycell_test-coordinator`

Create virtual environment and activate it
`python3 -m venv venv`
`source venv/bin/activate`

Install requirements
`pip3 install -r requirements.txt`

Install service and start it
```
sudo cp tinycell_test-coordinator.service /etc/systemd/system/tinycell_test-coordinator.service
sudo chown sixfab /etc/systemd/system/tinycell_test-coordinator.service
sudo systemctl daemon-reload
sudo systemctl enable tinycell_test-coordinator.service
sudo systemctl start tinycell_test-coordinator.service
```







