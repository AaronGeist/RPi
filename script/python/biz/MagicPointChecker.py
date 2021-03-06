# -*- coding:utf-8 -*-  

from biz import Secrets
from library.EmailSender import EmailSender
from library.Login import Login
from library.SiteRequest import SiteRequest
from library.Utils import Utils
import re


class MagicPointChecker:
    siteRequest = None

    POINT_THRESHOLD = 40

    def buildRequest(self):
        siteRequest = SiteRequest()
        siteRequest.baseUrl = "https://pt.sjtu.edu.cn/"
        siteRequest.homePage = "https://pt.sjtu.edu.cn/mybonus.php"
        siteRequest.loginPage = "https://pt.sjtu.edu.cn/login.php"
        siteRequest.loginPostPage = "https://pt.sjtu.edu.cn/takelogin.php"
        siteRequest.loginHeader = [
            ("User-Agent",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"),
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
            ("Accept-Language", "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2"),
            ("Content-Type", "application/x-www-form-urlencoded"),
            ("Host", "pt.sjtu.edu.cn"),
            ("Origin", "https://pt.sjtu.edu.cn"),
            ("DNT", "1"),
            ("Upgrade-Insecure-Requests", "1"),
            ("Referer",
             "https://pt.sjtu.edu.cn/login.php")
        ]
        siteRequest.userName = Secrets.siteUserName
        siteRequest.password = Secrets.sitePassword
        siteRequest.loginVerificationCss = "#userbar span.nobr a b"
        siteRequest.loginVerificationStr = siteRequest.userName

        return siteRequest

    def crawl(self):
        ret = self.login()
        assert ret

        soupObj = Utils.urlGet(self.siteRequest.homePage)
        return self.parsePoint(soupObj)

    def parsePoint(self, soupObj):
        assert soupObj is not None

        divList = soupObj.select("table.mainouter tr td table tr td div[align='center']")
        assert len(divList) == 1

        content = divList[0].contents[0]
        m = re.search(u"获取(\d+.\d+)个魔力", content)
        assert m
        return float(m.group(1))

    def login(self):
        request = self.buildRequest()
        self.siteRequest = request
        ret = Login.login(request)
        if ret:
            print("login,Y," + request.loginPage)
        else:
            print("login,N," + request.loginPage)

        return ret

    def notify(self, point):
        EmailSender.quickSend("魔力值警告: " + str(point), "")

    def check(self):
        point = self.crawl()
        if point <= MagicPointChecker.POINT_THRESHOLD:
            self.notify(point)


if __name__ == "__main__":
    checker = MagicPointChecker()
    checker.check()
