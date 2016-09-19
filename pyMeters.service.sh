#!/bin/bash

######
#Script to control pymeters process stopping and starting correctly

PID=`ps -ef | grep pyMeters | awk '{print $2}'`
COUNT=`wc -l $PID`

if $COUNT > 1
  then
    for i in PID;
      do
        echo "killing process: " $i
        kill -9 $i
      done
else
    echo "No process to kill"
fi

sudo python pyMetersWin10.py &

exit 0