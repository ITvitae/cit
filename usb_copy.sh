pmount /dev/sda1
sleep 1
curl localhost:5300 -o /media/sda1/index.html
sleep 1
pumount /dev/sda1

