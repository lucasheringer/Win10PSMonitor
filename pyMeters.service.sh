#!/bin/bash

######
#Script to control pymeters process stopping and starting correctly

PID=`ps -ef | grep python | awk '{print $2}'|head -n -1`
for i in $PID;
  do
    echo "killing process: " $i
    kill -9 $i
done

echo "starting pyMetersWin10"

sleep 2

python /home/pi/pyMetersWin10.py &

echo "is it working?"
