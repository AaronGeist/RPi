from biz import Secrets
from biz.SeedInfo import SeedInfo
from library.EmailSender import EmailSender
from library.Login import Login
from library.SiteRequest import SiteRequest
from library.Utils import Utils
import re


class ValuableSeedNotifier:
    siteRequest = None

    def buildRequest(self):
        siteRequest = SiteRequest()
        siteRequest.baseUrl = "https://pt.sjtu.edu.cn/"
        siteRequest.homePage = "https://pt.sjtu.edu.cn/torrents.php"
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
        return self.convertToSeed(soupObj)

    def convertToSeed(self, soupObj):
        assert soupObj is not None

        trList = soupObj.select("table.torrents tr")

        seedList = []
        cnt = 0
        for tr in trList:
            cnt += 1
            if cnt == 1:
                # skip the caption tr
                continue

            seed = SeedInfo()
            tdList = tr.select("td.rowfollow")
            if len(tdList) < 9:
                # skip embedded contents
                continue

            seed.title = tdList[1].select("table td a")[0]["title"]
            seed.url = self.siteRequest.baseUrl + tdList[1].select("table td a")[0]['href']
            seed.free = len(tdList[1].select("table font.free")) > 0
            seed.hot = len(tdList[1].select("table font.hot")) > 0
            seed.since = Utils.getContent(tdList[3], "span")
            seed.size = float(self.parseSize(tdList[4]))
            seed.uploadNum = int(self.getContentWithoutFontorStrong(tdList[5], "a"))
            seed.downloadNum = int(self.getContentWithoutFontorStrong(tdList[6], "a"))
            seed.finishNum = int(self.getContentWithoutFontorStrong(tdList[7], "a"))
            seed.id = self.parseId(seed.url)

            # print('\n'.join(['%s:%s' % item for item in seed.__dict__.items()]) + "\n")
            seedList.append(seed)

        return seedList

    def parseSize(self, soupObj):
        assert soupObj is not None
        assert len(soupObj.contents) == 3

        sizeNum = float(soupObj.contents[0])
        sizeUnit = soupObj.contents[2]

        if sizeUnit == "GB":
            return sizeNum * 1024
        if sizeUnit == "MB":
            return sizeNum
        if sizeUnit == "KB":
            return 0.01

    def getContentWithoutFontorStrong(self, soupObj, tag):
        assert soupObj is not None
        html = str(soupObj.contents[0])
        html = html.replace(',', '')
        m = re.search(">(\d+\.*\d?)<", html)
        if m:
            ret = m.group(1)
        else:
            ret = html
        return ret

    def parseId(self, url):
        m = re.search("id=(\d+)&", url)
        assert m is not None
        return m.group(1)

    def login(self):
        request = self.buildRequest()
        self.siteRequest = request
        ret = Login.login(request)
        if ret:
            print("login,Y," + request.loginPage)
        else:
            print("login,N," + request.loginPage)

        return ret

    def filter(self, seedList):
        result = []
        for seed in seedList:
            if seed.uploadNum != 0 and seed.downloadNum / seed.uploadNum >= 3:
                result.append(seed)
            elif seed.free and re.match("[0-2]时", "".join(seed.since)):
                result.append(seed)

        return result

    def notify(self, seedList):
        if len(seedList) == 0:
            return

        msg = ""
        for seed in seedList:
            msg += seed.litePrint()

        print(msg)

        EmailSender.quickSend(u"种子", msg)

    def check(self):
        seeds = self.crawl()
        filteredSeeds = self.filter(seeds)
        self.notify(filteredSeeds)

if __name__ == "__main__":
    seedNotifier = ValuableSeedNotifier()
    seedNotifier.check()
