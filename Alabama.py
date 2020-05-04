import random
import time
from builtins import print
import requests


from bs4 import BeautifulSoup

import SetProxy

# dateTest = "06/02/01"
# dateFormatted = datetime.datetime.strptime(dateTest, '%m/%d/%y')
# print(dateFormatted.date().strftime("%m-%d-%Y"))
nextBiz = 19996

baseURL = "http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?page=number&num1="
totalScraped = 0
formatted = ""
proxyCount = 0
count = 0


class Alabama:
    print(nextBiz)


def parse():
    # will need to catch or identify indexError
    f = open("Alabama.csv", "a")

    global nextBiz, totalScraped, count
    totalScraped += 1
    count += 1
    if totalScraped >= 65:
        SetProxy.renew_connection()
        totalScraped = 0

    #nextBiz = 6#random.randrange(400000)
    url = baseURL + str(nextBiz).zfill(
        6)
    print(url)

    session = SetProxy.get_tor_session(count)

    r = session.get(url)
    #r = requests.get(url)

    doc = BeautifulSoup(r.text, features="html.parser")
    #need to check if request have been limited before continuing

    status_check = 0

    for tag in doc.findAll():
        status_check += 1

    if status_check == 5:
        #set net proxy, reset count
        proxyCount = 0
        SetProxy.renew_connection()
        parse()

    if status_check == 406:
        #blank page, skip and recurse
        nextBiz += 1
        parse()
    length = 0
    desc = doc.find_all("td", class_="aiSosDetailDesc")
    value = doc.find_all("td", class_="aiSosDetailValue")
    name = doc.find_all("td", class_="aiSosDetailHead")
    for i, j in zip(desc, value):
        # print(i.text, end=" ")
        # print(" :::::::: ", end=" ")
        # print(j.text)
        pass


    print(name[0].text)
    print(desc[1].text)
    print(value[1].text)

    f.write(url + ", US, AL, " + '"' + name[0].text + '"' + ",\n")
    f.close()

    end = time.time() / 60
    time_elapsed = (end - start)
    request_per_minute = count / time_elapsed
    print("average request per minute", end=" ")
    print(round(request_per_minute, 2))
    nextBiz += 1

    parse()


global start
start = time.time() / 60
parse()
