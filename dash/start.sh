#!/bin/bash
sudo hciconfig hci0 up
sudo rmmod rfcomm
sudo modprobe rfcomm
sudo rfcomm bind rfcomm0 your_bluetooth_mac_address
ls /dev | grep rfcomm
sudo rfcomm listen /dev/rfcomm0 1 &
sudo python ./dash.py
echo "press any key!"
read -n 1
