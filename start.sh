sudo hciconfig hci0 up
sudo rmmod rfcomm
sudo modprobe rfcomm
sudo rfcomm bind rfcomm0 00:1D:A5:07:31:7A
ls /dev/ | grep rfcomm
sudo rfcomm listen /dev/rfcomm0 1 &
sudo python dash.py