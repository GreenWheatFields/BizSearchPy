import random
import time
from builtins import print

from bs4 import BeautifulSoup

import SetProxy

# dateTest = "06/02/01"
# dateFormatted = datetime.datetime.strptime(dateTest, '%m/%d/%y')
# print(dateFormatted.date().strftime("%m-%d-%Y"))
nextBiz = 1
csvWriter = open("Alabama.csv", "a")
baseURL = "http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?page=number&num1="
totalScraped = 0
formatted = ""
proxyCount = 0
count = 0


class Alabama:
    print(nextBiz)


def parse():
    # will need to catch or identify indexError
    global nextBiz, totalScraped, count
    totalScraped += 1
    count += 1
    if totalScraped >= 65:
        SetProxy.renew_connection()
        totalScraped = 0

    nextBiz = random.randrange(400000)
    url = baseURL + str(nextBiz).zfill(
        6)  # lack of 'add method, will probably mean parse, will pass through nextBiz directly
    print(url)

    session = SetProxy.get_tor_session(count)

    r = session.get(url)

    doc = BeautifulSoup(r.text, features="html.parser")
    desc = doc.find_all("td", class_="aiSosDetailDesc")
    value = doc.find_all("td", class_="aiSosDetailValue")
    name = doc.find_all("td", class_="aiSosDetailHead")
    for i, j in zip(desc, value):
        # print(i, end=" ")
        # print(" :::::::: ", end=" ")
        # print(j)
        pass

    print(name[0].string)
    print(value[9].string)
    print(count)
    end = time.time() / 60
    time_elapsed = (end - start)
    #print("time elapsed", end=" ")
    #print(time_elapsed)
    request_per_minute = count / time_elapsed
    print("average request per minute", end=" ")
    print(request_per_minute)
    nextBiz += 1
    parse()


global start
start = time.time() / 60
parse()
