#!/bin/bash
sudo rfcomm bind rfcomm0 your_bluetooth_mac_address
sudo rfcomm listen /dev/rfcomm0 1 &
sudo python ~/dash/dash.py
echo "press any key!"
read -n 1