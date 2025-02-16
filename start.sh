sudo hciconfig hci0 up
sudo rmmod rfcomm
sudo modprobe rfcomm
sudo rfcomm bind rfcomm0 01:23:45:67:89:BA
ls /dev/ | grep rfcomm
sudo rfcomm connect 0 01:23:45:67:89:BA 1&
sudo python dash.py