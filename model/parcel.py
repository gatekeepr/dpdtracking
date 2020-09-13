import requests

from bs4 import BeautifulSoup

TRACKING_URL = "http://www.fujexp.com:8082/en/trackIndex.htm"

class Parcel:
    tracking = None
    date = None
    status = None
    consignee = None
    alias = None
    owner = None

    def __init__(self, tracking, alias, owner):
        self.alias = alias
        self.tracking = tracking
        self.owner = owner
        resp = requests.get(TRACKING_URL + "?documentCode=" + str(self.tracking))
        print(resp.text)
        soup = BeautifulSoup(resp.text, "html.parser")
        elemCollect = soup.find_all("li")
        for elem in elemCollect:
            if(elem["class"][0] == "div_li3"):
                tmpDate = elem.string.strip()
            elif(elem["class"][0] == "div_li4"):
                self.status = elem.string
        tmpDate =  tmpDate[:-9].split("-")
        tmpDate.reverse()
        self.date = "-".join(tmpDate)
        self.consignee = soup.find_all("span")[0].string.strip()

    def __str__(self):
        return f"<{self.alias}> - {self.status} - [{self.date}]"

    def doUpdate(self):
        resp = requests.get(TRACKING_URL + "?documentCode=" + str(self.tracking))
        soup = BeautifulSoup(resp.text, "html.parser")
        elemCollect = soup.find_all("li")
        for elem in elemCollect:
            if(elem["class"][0] == "div_li3"):
                newDate = elem.string
            elif(elem["class"][0] == "div_li4"):
                newStatus = elem.string
        if(newStatus != self.status):
            self.status = newStatus
            self.date = newDate
            return True
        else:
            return False