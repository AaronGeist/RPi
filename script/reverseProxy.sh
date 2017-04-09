#!/bin/bash

sshStatus=`ps -ef|grep "104.207.153.248"|grep "8122"`
if [ -z "$sshStatus" ]; then
	ssh -fCNR 8122:localhost:22 shakazxx@104.207.153.248 & >/dev/null 2>&1
	echo "Reverse proxy creatd success!"
else
	echo "Reverse proxy already built!"
fi
