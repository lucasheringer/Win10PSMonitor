#!/bin/bash

######
#Script to control pymeters process stopping and starting correctly

PID=`ps -ef | grep pyMeters | awk '{print $2}'`
COUNT=`ps -ef | grep pyMeters | awk '{print $2}'|wc -l`

if [ $COUNT -gt 1 ]
  then
    for i in $PID;
      do
        echo "killing process: " $i
        kill -9 $i
      done
else
    echo "No process to kill"
fi

echo "starting pyMetersWin10"
python pyMetersWin10.py &

exit 0
