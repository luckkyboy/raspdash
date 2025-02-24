#!/bin/bash
sudo apt update && apt upgrade -y && apt full-upgrade -y
sudo apt install pip fonts-wqy-zenhei
sudo pip install pygame
sudo pip install git+https://github.com/luckkyboy/python-OBD.git
sudo git clone https://github.com/luckkyboy/raspdash.git
cd raspdash
sudo cp -rf ./dash ~/
sudo chmod 777 ~/dash/*
sudo mkdir ~/.config/autostart
sudo cp -f ./dash.desktop ~/.config/autostart/dash.desktop