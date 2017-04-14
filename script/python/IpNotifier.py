import os

from library.EmailSender import EmailSender

output = os.popen("curl ip.gs | awk '{print $2}' | awk -F'：' '{print $2}'")
ip = output.read().strip()

EmailSender.quickSend(u"最新IP: " + str(ip), "")
