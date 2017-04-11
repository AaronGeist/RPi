class SiteRequest:

    baseUrl = ""
    homePage = ""

    needLogin = True
    userName = ""
    password = ""
    loginPage = ""
    loginPostPage = ""
    loginHeader = ""
    loginVerificationStr = ""
    loginVerificationCss = ""




    BASE_URL = "http://weibo.cn/"
    HOME_PAGE = BASE_URL
    LOGIN_PAGE = "http://login.weibo.cn/login/?rand=1640789743&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%E5%BE%AE%E5%8D%9A&vt=4&revalid=2&ns=1"
    LOGIN_HEADERS = [
                ("User-Agent",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"),
                ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
                ("Accept-Language", "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2"),
                ("Content-Type", "application/x-www-form-urlencoded"),
                ("Host", "login.weibo.cn"),
                ("Origin", "http://login.weibo.cn"),
                ("DNT", "1"),
                ("Upgrade-Insecure-Requests", "1"),
                ("Referer",
                 "http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=4")
            ]

    NEED_LOGIN = True
    LOGIN_INDICATOR_CSS = "div.u > div.ut"
    LOGIN_VERIFICATION_STR = "奏乐爱做俯卧飞鸟"
    USERNAME = ""
    PASSWORD = ""