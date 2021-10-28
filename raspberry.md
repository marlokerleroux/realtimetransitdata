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
## File

```bash
/
├── etc
│   └──  systemd
│        └── system
│            └── projet.service
├── opt
│   └── projet
│       ├── Fonts
│       │   ├── 5x8.bdf
│       │   ├── 5x8.bdf
│       │   └── 5x8.bdf
│       ├── main.py
│       ├── samplebase.py
│       └── moduleEcran.py
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
```
$ systemctl daemon-reload
```

## Web

1. Vérifier MAJ
```
sudo apt update
sudo apt upgrade
sudo apt update
```
2. Installer Apache
```
sudo apt install apache2
```
3. Définir droits dossier Apache
```
sudo chown -R pi:www-data /var/www/html/
sudo chmod -R 770 /var/www/html/
```
4. Vérifier que le serveur fonctionne sur http://127.0.0.1

5. Si pas d'interface graphique, faire :
```
wget -O verif_apache.html http://127.0.0.1
```
6. Tjrs si pas d'interface graphique : vérifier que ce fichier contient "It works"
```
cat ./verif_apache.html
```
7. Installer PHP
```
sudo apt install php php-mbstring
