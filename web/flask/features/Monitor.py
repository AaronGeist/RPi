import redis
import os
import json
import time
import datetime


class Database:
    instance = None
    MAX_SIZE = 2000

    def __init__(self):
        if self.instance is None:
            pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
            self.instance = redis.StrictRedis(connection_pool=pool)

    def append(self, bucketName, value):
        if self.instance.llen(bucketName) == self.MAX_SIZE * 2:
            self.instance.ltrim(bucketName, 0, self.MAX_SIZE - 1)
        self.instance.lpush(bucketName, value)

    def getByRange(self, bucketName, start=0, end=-1):
        return self.instance.lrange(bucketName, start, end)

    def show(self, bucketName):
        print(self.instance.lrange(bucketName, 0, -1))


class Config:
    PATH = "config.json"

    innerConfig = None

    @staticmethod
    def init():
        with open(Config.PATH, 'r') as f:
            Config.innerConfig = json.load(f)

    @staticmethod
    def get(attr):
        if Config.innerConfig is None:
            Config.init()
        return Config.innerConfig[attr]


class BaseMonitor(object):
    bucketName = ""
    cmd = ""
    db = Database()

    # max size per fetch
    LIMIT = 20
    DELIMITER = "_"

    def __init__(self, bucketName, command):
        self.bucketName = bucketName
        self.cmd = command

    def history(self):
        res = dict()
        data = list()
        title = list()
        for single in self.db.getByRange(self.bucketName, start=0, end=self.LIMIT):
            item = single.split(self.DELIMITER)
            title.append(item[0])
            data.append(float(item[1]))
        data.reverse()
        title.reverse()
        res['data'] = data
        res['title'] = title
        return res

    def latest(self):
        res = dict()
        for single in self.db.getByRange(self.bucketName, start=0, end=0):
            item = single.split(self.DELIMITER)
            res['title'] = item[0]
            res['data'] = float(item[1])
            break
        return res

    def monitor(self):
        output = os.popen(self.cmd).read()
        now = datetime.datetime.now()
        self.db.append(self.bucketName, now.strftime('%H:%M:%S') + "_" + str(output))


class CpuTemperature(BaseMonitor):
    CPU_TEMP_BUCKET = "cpu_temperature"

    def __init__(self):
        super(CpuTemperature, self).__init__(self.CPU_TEMP_BUCKET, "")

    def monitor(self):
        with open("/sys/class/thermal/thermal_zone0/temp") as tempFile:
            res = tempFile.read()
            res = str(float(res) / 1000)

        now = datetime.datetime.now()
        self.db.append(self.bucketName, now.strftime('%H:%M:%S') + "_" + str(res))


class Memory(BaseMonitor):
    MEMORY_BUCKET = "memory"
    CMD = "free -m | grep buffers/cache | awk '{print $3}'"

    def __init__(self):
        super(Memory, self).__init__(self.MEMORY_BUCKET, self.CMD)


if __name__ == '__main__':
    try:
        interval = Config.get("monitor_interval")
        while True:
            CpuTemperature().monitor()
            Memory().monitor()
            time.sleep(interval)
    except KeyboardInterrupt:
        pass

