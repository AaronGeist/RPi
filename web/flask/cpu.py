import redis
import os
import time

def getCPUtemperature():
	with open("/sys/class/thermal/thermal_zone0/temp") as tempFile:
		res = tempFile.read()
		res=str(float(res)/1000)
	return res

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.StrictRedis(connection_pool=pool)

for i in range(0, 3):
	temp = getCPUtemperature()
	print(temp)
	r.rpush("cpu_temp", temp)
	time.sleep(1)

print(r.lrange("cpu_temp",0,-1))


