#!/bin/bash
#Script to control pymeters process stopping and starting correctly
#python /home/pi/pyMetersWin10.py >/dev/null

case "$1" in
start)
   python /home/pi/pyMetersWin10.py &
   echo $!>/var/run/pyMeters.pid
   ;;
stop)
   kill -9 `cat /var/run/pyMeters.pid`
   rm /var/run/pyMeters.pid
   ;;
restart)
   $0 stop
   $0 start
   ;;
status)
   if [ -e /var/run/pyMeters.pid ]; then
      echo pyMetersWin10.py is running, pid=`cat /var/run/pyMeters.pid`
   else
      echo pyMetersWin10.py is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0
