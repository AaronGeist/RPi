#!/bin/bash

check_connection() {
	conn=`nc -w 1 104.207.153.248 8022|grep SSH`
	if [ -z "$conn" ]; then
		return 1
	else
		return 0
	fi
}

res=check_connection
if "$res"; then
	echo "Reverse proxy already existed!"
	exit 0
else
	echo "Reverse proxy not existed!"
fi

for i in {1..3}
do
	ps -ef|grep "104.207.153.248"|grep "8122"|awk '{print $2}'|xargs kill -9
	ssh -fCNR 8122:localhost:22 shakazxx@104.207.153.248 & >/dev/null 2>&1
	sleep 5
	res=check_connection
	if "$res"; then
                echo "Reverse proxy created success!"
		exit 0
	else
		echo "Reverse proxy created fail!"
	fi
done
exit 0
