# Raspberry
## User
 - user: pi
 - password: isengroupB%
## SSH
  - port: 22
  - user: pi
  - password: isengroupB%

## Install
 - Raspberrypi Imager

 - init
 ```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python3
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh
```
## Service
'/etc/systemd/system/projet.service'
```
[Unit]
Description=ProjetEcranBus
After=network-online.target

[Service]
Type=simple

User=pi
Group=pi
UMask=007

ExecStart=/usr/bin/python3 /opt/projet/main.py

Restart=on-failure

# Configures the time to wait before service is stopped forcefully.
TimeoutStopSec=300

[Install]
WantedBy=multi-user.target
```
