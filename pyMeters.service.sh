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
pyPID=`sudo python pyMetersWin10.py &`

echo $pyPID

exit 0
