#!/bin/bash

while true
do
  IDLECPU=`top -b -n2 | grep "Cpu(s)" | awk '{print $8}'|tail -1`
  CPU=`echo "100-"$IDLECPU | bc`
  FREE_DATA=` free -m | grep Mem`
  CURRENT=`echo $FREE_DATA | cut -f3 -d' '`
  TOTAL=`echo $FREE_DATA | cut -f2 -d' '`
  RAM=$(echo "scale = 2; $CURRENT/$TOTAL*100" | bc)
  HDD=`df -lh | awk '{if ($6 == "/") { print $5 }}' | head -1 | cut -d'%' -f1`
  DISKIO=`iostat -x -d -y  sda2 1 2|tail -2`
  DISK=`echo $DISKIO|cut -d " " -f 14`
  CPUTEMP=`sensors -Au|grep temp1_input| awk '{print $2}'|tail -1`
  CPUFAN=`cat /proc/acpi/ibm/fan |grep speed |awk '{print $2}'`

  echo "{\"cols\": "  > /var/www/html/results.json
  echo "[{\"id\":\"String\",\"label\":\"String\",\"type\":\"string\"}," >> /var/www/html/results.json
  echo "{\"id\":\"Value\",\"label\":\"Value\",\"type\":\"number\"}]," >> /var/www/html/results.json
  echo "\"rows\" : [" >> /var/www/html/results.json
  echo "{\"c\":[{\"v\":\"CPU\"},{\"v\" : " $CPU "}]},">> /var/www/html/results.json
  echo "{\"c\":[{\"v\":\"Memory\"},{\"v\" : "$RAM "}]},">> /var/www/html/results.json
  echo "{\"c\":[{\"v\":\"Disk\"},{\"v\" : "$DISK "}]},">> /var/www/html/results.json
  echo "{\"c\":[{\"v\":\"CPUTemp\"},{\"v\" : "$CPUTEMP "}]},">> /var/www/html/results.json
  echo "{\"c\":[{\"v\":\"CPUFAN\"},{\"v\" : "$CPUFAN "}]}">> /var/www/html/results.json
  echo "]}" >> /var/www/html/results.json
  sleep 1
done
