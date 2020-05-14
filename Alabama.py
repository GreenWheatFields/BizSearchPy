import random
import time
import requests
import datetime

from bs4 import BeautifulSoup

import SetProxy

nextBiz = 3297

baseURL = "http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?page=number&num1="
totalScraped = 0
formatted = ""
proxyCount = 0
count = 0
errorCount = 0
global start
start = time.time() / 60
totalCount = 0
print(nextBiz)


def find_foreign_company(desc, value, name):
    for i in value:
        for j in desc:
            if "Foreign" in i.text and "Legal Name in Place of Origin" in j.text:
                print("origin includeds")
                value.pop(1)
                # im not sure if one is consitently to location, it could be a bug in the future
                return value


def parse():
    # will need to catch or identify indexError

    f = open("Alabama.csv", "a")

    global nextBiz, totalScraped, count, start, totalCount, errorCount
    nextBiz += 1
    totalScraped += 1
    count += 1
    if totalCount >= 950000:
        kill_switch()

    if totalScraped >= 70:
        SetProxy.renew_connection()
        totalScraped = 0

    url = baseURL + str(nextBiz).zfill(6)
    print(url)
    session = SetProxy.get_tor_session()

    r = session.get(url)
    # r = requests.get(url)

    doc = BeautifulSoup(r.text, features="html.parser")

    # need to check if request have been limited before continuing

    status_check = 0

    for tag in doc.findAll():
        status_check += 1

    if status_check == 5:
        # set net proxy, reset count
        proxyCount = 0
        SetProxy.renew_connection()
        parse()

    if status_check == 406:
        # blank page, skip and recurse
        nextBiz += 1
        parse()
    length = 0
    desc = doc.find_all("td", class_="aiSosDetailDesc")
    value = doc.find_all("td", class_="aiSosDetailValue")
    name = doc.find_all("td", class_="aiSosDetailHead")
    f.write(url + ", US, AL, " + '"' + name[0].text + '"' + ",")  # name and constant variables

    print(name[0].text)
    f.write(value[0].text + ',')  # entity number

    find_foreign_company(desc, value, name)

    f.write(value[1].text + ",")  # official business type

    # get the core business type
    if "Foreign" in value[1].text:
        f.write("Foreign ")
    elif "Foreign" not in value[1].text:
        f.write("Domestic ")
    if "Limited" in value[1].text:
        f.write("LLC,")
    elif "Corporation" in value[1].text:
        f.write("Corporation,")
    else:
        f.write("---,")

    f.write(value[4].text + ",")  # status
    # First major split in the structure of the elements. For example, companies that don't exist have an entry of when they stopped existing, companies that do exist, don't.
    if value[4].text == "Dissolved":
        try:
            dateFormatted = datetime.datetime.strptime(value[5].text.strip(), '%m-%d-%Y')
            f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # dissolve date
            dateFormatted = datetime.datetime.strptime(value[7].text.replace(" ", ""), '%m-%d-%Y')
            f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # formation date
        except ValueError:
            f.write("---,---,")
        f.write('"' + value[8].text.replace("\n", "").strip() + '",')  # registerered agent name
        f.write('"' + value[9].text.replace("\n", "").strip() + '",')  # registerered office add.
        f.write('"' + value[10].text.replace("\n", "").strip() + '",' + "\n")  # registerered mailing add.
        f.close()
        totalScraped += 1
        totalCount += 1
        print("Total: ", end=" ")
        print(totalCount)
        get_request_per_minute()
        # print(totalScraped) add a global counter
        parse()

    elif value[4].text == "Withdrawn":
        try:
            dateFormatted = datetime.datetime.strptime(value[5].text.strip(), '%m-%d-%Y')
            f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # withdraw date
            dateFormatted = datetime.datetime.strptime(value[8].text.replace(" ", ""), '%m-%d-%Y')
            f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # formation date
        except ValueError:
            f.write("---,---,")
        f.write('"' + value[10].text.replace("\n", "").strip() + '",')  # reg agent name
        f.write('"' + value[11].text.replace("\n", "").strip() + '",')  # reg address
        f.write('"' + value[12].text.replace("\n", "").strip() + '",\n')  # reg mailing
        f.close()
        totalScraped += 1
        totalCount += 1
        print("Total: ", end=" ")
        print(totalCount)
        get_request_per_minute()
        parse()
    elif value[4].text == "Exists":
        f.write("---,")
        try:
            dateFormatted = datetime.datetime.strptime(value[6].text.strip(), '%m-%d-%Y')
            f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # formation date
        except ValueError:
            f.write("---,")
        f.write('"' + value[7].text.replace("\n", "").strip() + '",')  # reg name, add., mail add.
        f.write('"' + value[8].text.replace("\n", "").strip() + '",')
        f.write('"' + value[9].text.replace("\n", "").strip() + '",\n')
        f.close()
        totalCount += 1
        print("Total: ", end=" ")
        print(totalCount)
        get_request_per_minute()
        totalScraped += 1
        parse()
    elif value[4].text == "Merged" or "Consolidated":
        try:
            dateFormatted = datetime.datetime.strptime(value[5].text.strip(), '%m-%d-%Y')
            f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # change date date
            dateFormatted = datetime.datetime.strptime(value[8].text.replace(" ", ""), '%m-%d-%Y')
            f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # formation date
        except ValueError:
            f.write("---,---,")
        f.write('"' + value[9].text.replace("\n", "").strip() + '",')  # reg name, add., mail add.
        f.write('"' + value[10].text.replace("\n", "").strip() + '",')
        f.write('"' + value[11].text.replace("\n", "").strip() + '",\n')
        f.close()
        totalScraped += 1
        totalCount += 1
        print("Total: ", end=" ")
        print(totalCount)
        get_request_per_minute()
        parse()
    elif value[4].text == "Cancelled":
        f.write('"MANUAL_REVIEW_REQUIRED\n')
        f.close()
        totalScraped += 1
        totalCount += 1
        print("Total: ", end=" ")
        print(totalCount)
        get_request_per_minute()
        parse()
    else:
        f.write('"MANUAL_REVIEW_REQUIRED\n')
        f.close()
        totalScraped += 1
        totalCount += 1
        print("Total: ", end=" ")
        print(totalCount)
        get_request_per_minute()
        parse()


def get_request_per_minute():
    end = time.time() / 60
    time_elapsed = (end - start)
    request_per_minute = count / time_elapsed
    print("average request per minute", end=" ")
    print(round(request_per_minute, 2))


def kill_switch():
    print("Done")


parse()
