from instapush import Instapush, App


class InstapushWrapper:
    app = None

    @staticmethod
    def initialize():
        if InstapushWrapper.app is None:
            InstapushWrapper.app = App(appid="58f89476a4c48af791967a04", secret="6a68c98f654efb6547d299c5ded84dbb")


    @staticmethod
    def notify(eventName, trackers):
        InstapushWrapper.initialize()
        InstapushWrapper.app.notify(event_name=eventName, trackers=trackers)

