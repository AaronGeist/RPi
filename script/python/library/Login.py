from library.SiteRequest import SiteRequest
from library.Utils import Utils


class Login:
    # login status cache
    isLogin = False

    @staticmethod
    def login(siteRequest):
        if siteRequest.needLogin and not Login.isLogin and not Login.checkLogin(siteRequest):
            res = Utils.urlPost(siteRequest.loginPostPage, data=Login.buildPostData(siteRequest),
                                headers=siteRequest.loginHeader, returnRaw=True)
            print("PostLoginData,", res.status, res.reason)

            Utils.saveCookie()
            Login.isLogin = Login.checkLogin(siteRequest)
            return Login.isLogin
        else:
            Login.isLogin = True
            return True

    @staticmethod
    def buildPostData(siteRequest):
        # soupPage = Utils.urlGet(siteRequest.loginPage)
        # assert soupPage is not None
        #
        # pwKey = soupPage.select('input[type="password"]')[0]['name']
        # vkValue = soupPage.select('input[name="vk"]')[0]['value']
        # capId = soupPage.select('input[name="capId"]')[0]['value']
        # captchaSrc = soupPage.select('form > div > img')[0]['src']
        # print("captcha url=" + captchaSrc)
        #
        # captcha = input("Input your id plz:\n")

        data = dict()
        data['username'] = siteRequest.userName
        data['password'] = siteRequest.password
        data['checkcode'] = "XxXx"

        return data

    @staticmethod
    def checkLogin(siteRequest):
        content = Utils.getContent(Utils.urlGet(siteRequest.homePage), siteRequest.loginVerificationCss)
        return content is not None and content == siteRequest.loginVerificationStr
