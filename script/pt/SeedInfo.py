class SeedInfo:
    id = ""
    title = ""
    url = ""
    size = 0
    downloadNum = 0
    uploadNum = 0
    finisheNum = 0
    hot = False
    free = False
    discount = 0
    discountTtl = ""
    since = ""

    def litePrint(self):
        msg = []
        if self.free:
            msg.append("Y")
        else:
            msg.append("N")

        msg.append(str(self.uploadNum))
        msg.append(str(self.downloadNum))
        msg.append(self.since)
        msg.append(str(int(self.size / 1024)))

        return "|".join(msg) + '\n'
