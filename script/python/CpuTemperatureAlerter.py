import os

from library.EmailSender import EmailSender

output = os.popen("vcgencmd measure_temp| awk -F= '{print $2}'| awk -F\"'\" '{print $1}'")
temperature = output.read().strip()

if float(temperature) > 50:
    EmailSender.quickSend(u"发烧啦: " + str(temperature), "")
