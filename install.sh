#!/bin/bash
sudo apt update && apt upgrade -y && apt full-upgrade -y
sudo apt install python3 python3-pip fonts-wqy-zenhei
sudo pip install pygame
sudo pip install git+https://github.com/luckkyboy/python-OBD.git
sudo git clone https://github.com/luckkyboy/raspdash.git
cd raspdash
sudo cp -rf ./dash ~/
sudo chmod 777 ~/dash && chmod 777 ~/dash/*
sudo mkdir ~/.config && mkdir ~/.config/autostart
sudo cp ./dash.desktop ~/.config/autostart/dash.desktop
cd ..
rm -rf ./raspdash
echo "Done, pls check and reboot this device!"