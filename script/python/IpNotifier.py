import os

from library.EmailSender import EmailSender

FILE = "/var/tmp/ip.txt"
oldIp = ""

if os.path.exists(FILE):
    with open(FILE, "r") as fp:
        oldIp = fp.readline().strip()

output = os.popen("curl ip.gs | awk '{print $2}' | awk -F'：' '{print $2}'")
newIp = output.read().strip()

if oldIp != newIp:
    with open(FILE, "w") as fp:
        fp.writelines(newIp)
    print("old[%s], new[%s]" % (oldIp, newIp))
    EmailSender.quickSend(u"最新IP: " + str(newIp), "")
else:
    print("same ip[%s]" % oldIp)

