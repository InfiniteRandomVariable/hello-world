#!/bin/bash

NAME="selenium_node"
LOG_FILE="/tmp/$NAME.log"
BASE="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb"
PID_FILE="$BASE/hello-world/selenium/$NAME.pid"
SEL_SERVER="$BASE/selenium-server-standalone-2.44.0.jar"
CONFIG="$BASE/hello-world/selenium/hubConfig.json"


#PID_FILE="/var/run/$NAME.pid"
#SEL_SERVER="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/selenium-server-standalone-2.44.0.jar"
#CONFIG="/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/hubConfig.json"
HOST="http://localhost:4444/grid/register"

#INIT_NODE="java -jar $SEL_SERVER -role node -hub $HOST -cleanupCycle 60000"
INIT_NODE="java -jar $SEL_SERVER -role node -hub $HOST"

function startprocedure {
      # echo $! > $PID_FILE;
	# don't use jsp-l kill process coz it may kill the hub process

	pkill firefox-bin
	kill `cat $PID_FILE` && rm -f $PID_FILE
	echo $$ > $PID_FILE
	$INIT_NODE & 1>/tmp/$NAME.out
        #exec 2>&1 $INIT_NODE 1>/tmp/$NAME.out
}

function stopprocedure {
        # try to kill the process by file and delete the file, else use jps to kill the process
        pkill firefox-bin
        kill `cat $PID_FILE` && rm -f $PID_FILE || jps -l | grep $SEL_SERVER | cut -d ' ' -f 1 | xargs -n1 kill
}


 case $1 in
    	start)
		startprocedure;;
     	stop)
		stopprocedure;;
	restart)
		stopprocedure
		startprocedure;;
     *)  
	echo "usage: $NAME {start|stop}" ;;
 esac
 exit 0
