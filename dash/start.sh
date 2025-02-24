#!/bin/bash
sudo rfcomm bind rfcomm0 00:1D:A5:07:31:7A
sudo rfcomm listen /dev/rfcomm0 1 &
sudo python ~/dash/dash.py
echo "press any key!"
read -n 1