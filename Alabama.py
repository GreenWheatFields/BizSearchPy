import random
import time
from builtins import print
import requests
import datetime


from bs4 import BeautifulSoup

import SetProxy

dateTest = "06/02/01"

nextBiz = 18554

baseURL = "http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?page=number&num1="
totalScraped = 0
formatted = ""
proxyCount = 0
count = 0


class Alabama:
    print(nextBiz)

def find_foreign_company(desc, value):
    for i, j in zip(desc,value):
        if "Entity Type" in i.text.replace("\n", "").strip():
            if "Foreign" in j.text.replace("\n", "").strip():
                f2 = open("Alabama.csv", "a")
                f2.write("Manualreview,\n")

                #totalScraped += 1 replcae with global count variable
                print("foregin company")
                f2.close()
                parse()
def parse():
    # will need to catch or identify indexError

    f = open("Alabama.csv", "a")


    global nextBiz, totalScraped, count
    nextBiz += 1
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


   # print(name[0].text)
    #print(desc[1].text)
    #print(value[1].text)

    f.write(url + ", US, AL, " + '"' + name[0].text + '"' + ",") #name and constant variables
    print(name[0].text)
    f.write(value[0].text + ',') #entity number

    find_foreign_company(desc,value)



    f.write(value[1].text + ",")
    print(value[1].text)

    # get the core business type
    if "Limited" in value[1].text:
        f.write("LLC,")
    elif "Corporation" in value[1].text:
        f.write("Corporation,")
    else:
        f.write("---,")

    # if "Exit" in value[3].text:
    #     f.write("Foreign,")
    #     print('test')
    #     totalScraped += 1
    #     parse()


    f.write(value[4].text + ",") #status

    if value[4].text == "Dissolved":
        dateFormatted = datetime.datetime.strptime(value[5].text.strip(), '%m-%d-%Y')
        f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",") # dissolve date
        dateFormatted = datetime.datetime.strptime(value[7].text.replace(" ", ""), '%m-%d-%Y')
        f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  #formation date
        f.write('"' + value[8].text.replace("\n", "").strip() + '",') #registerered agent name
        f.write('"' + value[9].text.replace("\n", "").strip() + '",')  # registerered office add.
        f.write('"' + value[10].text.replace("\n", "").strip() + '",' + "\n")  # registerered mailing add.
        f.close()
        totalScraped += 1
        #print(totalScraped) add a global counter
        parse()

    elif value[4].text == "Withdrawn":
        dateFormatted = datetime.datetime.strptime(value[5].text.strip(), '%m-%d-%Y')
        f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # dissolve date
        dateFormatted = datetime.datetime.strptime(value[8].text.replace(" ", ""), '%m-%d-%Y')
        f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # formation date
        f.write('"' + value[10].text.replace("\n", "").strip() + '",') #reg agent name
        f.write('"' + value[11].text.replace("\n", "").strip() + '",') #reg address
        f.write('"' + value[12].text.replace("\n", "").strip() + '",\n') #reg mailing
        f.close()
        totalScraped += 1
        parse()
    elif value[4].text == "Exists":
        f.write("---,")
        dateFormatted = datetime.datetime.strptime(value[6].text.strip(), '%m-%d-%Y')
        f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",") #formation date
        f.write('"' + value[7].text.replace("\n", "").strip() + '",')   # reg name, add., mail add.
        f.write('"' + value[8].text.replace("\n", "").strip() + '",')
        f.write('"' + value[9].text.replace("\n", "").strip() + '",\n')
        f.close()
        totalScraped += 1
        parse()
    elif value[4].text == "Merged" or "Consolidated":
        dateFormatted = datetime.datetime.strptime(value[5].text.strip(), '%m-%d-%Y')
        f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # change date date
        dateFormatted = datetime.datetime.strptime(value[8].text.replace(" ", ""), '%m-%d-%Y')
        f.write(dateFormatted.date().strftime("%m/%d/%Y") + ",")  # formation date
        f.write('"' + value[9].text.replace("\n", "").strip() + '",')  # reg name, add., mail add.
        f.write('"' + value[10].text.replace("\n", "").strip() + '",')
        f.write('"' + value[11].text.replace("\n", "").strip() + '",')
        f.close()
        totalScraped += 1
        parse()
    elif value[4].text == "Cancelled":
        f.write('"MANUAL_REVIEW_REQUIRED')
        f.close()
        totalScraped += 1
        parse()



    print(value[9].text)






    end = time.time() / 60
    time_elapsed = (end - start)
    request_per_minute = count / time_elapsed
    print("average request per minute", end=" ")
    print(round(request_per_minute, 2))

    f.close()
    parse()


global start
start = time.time() / 60
parse()
