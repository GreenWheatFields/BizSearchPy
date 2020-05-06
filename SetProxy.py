import requests
import Keys
import json
from stem import Signal
from stem.control import Controller

global count
count = 0

def get_tor_session():
    global session, count
    count += 1

    session = requests.session()
    session.proxies = {'http': Keys.tor_proxy(),
                       'https': Keys.tor_proxy()}
    if count == 1:
        print("Connected to TOR proxy")
        print("Getting IP")
        ip = json.loads(session.get("http://httpbin.org/ip").text)
        print(ip["origin"])
        print("Getting location")
        location_url = "https://ipapi.co/" + ip["origin"] + "/json/"
        location = json.loads(requests.get(location_url).text)
        print(location["country_name"])
        count += 1
    return session


def renew_connection():
    print("getting new TOR connection")

    with Controller.from_port(port=Keys.tor_port()) as controller:
        controller.authenticate(password=Keys.tor_pass())
        controller.signal(Signal.NEWNYM)
        print("New TOR connection")
        print(session.get("http://httpbin.org/ip").text)
        # would like to log the location as well as the ip, or just create at log for data analysis
        # speeds request per minute etc.
        # time between switching, etc
        # perhaps to increase speed, look into opening multiple instances
