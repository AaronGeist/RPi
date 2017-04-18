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

r.flushdb()
max_size = 10

def append(redis, bucket, value):
	if (redis.llen(bucket) == max_size * 2):
		print(r.lrange("cpu_temp",0,-1))
		redis.ltrim(bucket, 0, max_size - 1)
		print(r.lrange("cpu_temp",0,-1))
	redis.lpush(bucket, value)

for i in range(0, 25):
	#temp = getCPUtemperature()
	append(r, "cpu_temp", i)

print(r.lrange("cpu_temp",0,-1))


