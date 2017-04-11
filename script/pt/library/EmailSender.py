import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class EmailSender:
    @staticmethod
    def formatAddr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    @staticmethod
    def buildMsg(email):
        msg = MIMEText(email.body, 'plain', 'utf-8')
        msg['From'] = EmailSender.formatAddr(u'自己 <%s>' % email.fromAddr)
        msg['To'] = EmailSender.formatAddr(u'自己 <%s>' % email.toAddr)
        msg['Subject'] = Header(u'通知', 'utf-8').encode()

        return msg

    @staticmethod
    def send(email):
        msg = EmailSender.buildMsg(email)
        server = smtplib.SMTP(email.stmpServer, 25)
        server.set_debuglevel(1)
        server.login(email.fromAddr, email.password)
        server.sendmail(email.fromAddr, email.toAddr, msg.as_string())
        server.quit()
